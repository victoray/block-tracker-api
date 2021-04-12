import json
from contextlib import suppress
from typing import List

from assets.db import collection as asset_collection
from assets.models import Asset
from balance.db import collection as balance_collection
from balance.models import Balance
from price.coinmarketcap import get_latest_price
from transactions.db import collection as transaction_collection
from transactions.models import Transaction

with open("coinlist.json") as f:
    coin_list: dict = json.load(f)


def get_transaction_objects(docs: List[dict]) -> List[Transaction]:
    transactions = []

    for doc in docs:
        doc["id"] = str(doc.pop("_id"))
        doc["coin"] = coin_list.get("Data", {}).get(doc["assetId"])
        transactions.append(Transaction.parse_obj(doc))

    return transactions


def calculate_balance(user_id: str, asset_id=None):
    query = {"userId": user_id}

    if asset_id:
        query.update(id=asset_id)

    result = asset_collection.find(query)
    assets: List[Asset] = []
    for doc in result:
        assets.append(Asset.parse_obj(doc))

    current_value = sum(map(lambda a: a.currentValue, assets))
    original_value = sum(map(lambda a: a.originalValue, assets))
    balance = Balance(
        amount=current_value,
        change=calculate_pnl_percent(original_value, current_value),
        userId=user_id,
        assetId=asset_id,
    )
    if asset_id:
        query["assetId"] = query.pop("id")
    return balance_collection.find_one_and_update(
        query, {"$set": balance.dict()}, upsert=True
    )


def calculate_asset_pnl(transactions: List[Transaction], asset_id: str):
    current_value = 0
    original_value = 0

    with suppress(Exception):
        current_price = None
        current_price = get_latest_price(asset_id).priceUSD

    if current_price:
        for transaction in transactions:
            current_value += float(current_price) * transaction.amount
            original_value += transaction.price * transaction.amount

    return (
        current_value,
        original_value,
        calculate_pnl_percent(original_value, current_value),
    )


def aggregate_asset(transactions: List[Transaction], user_id: str):
    groups: dict = {}
    for transaction in transactions:
        groups[transaction.assetId] = groups.get(transaction.assetId, []) + [
            transaction
        ]

    assets = []

    for asset, transactions in groups.items():
        with suppress():
            price = "-"
            price = get_latest_price(asset).priceUSD

        current_value, original_value, pnl_percent = calculate_asset_pnl(
            transactions, asset
        )

        asset = Asset(
            id=asset,
            name=coin_list.get("Data", {}).get(asset, {}).get("CoinName"),
            coin=coin_list.get("Data", {}).get(asset, {}),
            price=price,
            amount=sum(map(lambda x: x.amount, transactions)),
            currentValue=current_value,
            originalValue=original_value,
            pnl=current_value - original_value,
            pnlPercent=pnl_percent,
            userId=user_id,
        )
        assets.append(asset.dict())

    for asset in assets:
        asset_collection.update_one(
            {"id": asset.get("id"), "userId": user_id}, {"$set": asset}, upsert=True
        )


def calculate_pnl_percent(original_value: float, current_value: float):
    if not original_value:
        return 0

    change = (current_value / original_value) * 100
    return change - 100


def calculate_pnl(transaction: Transaction, save=False):
    price = transaction.price
    with suppress(Exception):
        current_price = None
        current_price = get_latest_price(transaction.assetId).priceUSD

    if current_price:
        amount = (
            transaction.amount * -1
            if transaction.type == Transaction.Type.REMOVE and Transaction.amount > 0
            else transaction.amount
        )
        current_value = amount * float(current_price)
        original_value = amount * price
        transaction.pnl = current_value - original_value
        transaction.pnlPercent = calculate_pnl_percent(original_value, current_value)
        if save:
            transaction.save()

    return transaction


def aggregate_transactions(transaction_filter=None):
    if transaction_filter is None:
        transaction_filter = {}
    transactions = transaction_collection.find(transaction_filter)
    transaction_objects = [
        calculate_pnl(Transaction.parse_obj(t), save=True)
        for t in get_transaction_objects(transactions)
    ]
    aggregate_asset(transaction_objects, user_id=transaction_filter.get("userId"))


def update_assets(transaction: Transaction, user_id: str):

    transaction_count = transaction_collection.count_documents(
        {"userId": user_id, "assetId": transaction.assetId}
    )
    if not transaction_count:
        asset_collection.delete_one({"userId": user_id, "id": transaction.assetId})
