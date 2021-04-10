import json
from contextlib import suppress
from typing import List

from assets.db import collection as asset_collection
from assets.models import Asset
from price.coinmarketcap import get_latest_price
from transactions.db import collection as transaction_collection
from transactions.models import Transaction
from transactions.utils import get_transaction_objects

with open("coinlist.json") as f:
    coin_list: dict = json.load(f)


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


def aggregate_asset(transactions: List[Transaction]):
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
            pnl=current_value - original_value,
            pnlPercent=pnl_percent,
        )
        assets.append(asset.dict())

    for asset in assets:
        asset_collection.update_one(
            {"id": asset.get("id")}, {"$set": asset}, upsert=True
        )


def calculate_pnl_percent(original_value: float, current_value: float):
    change = (current_value / original_value) * 100
    return change - 100


def calculate_pnl(transaction: Transaction, save=False):
    price = transaction.price
    with suppress(Exception):
        current_price = None
        current_price = get_latest_price(transaction.assetId).priceUSD

    if current_price:
        current_value = transaction.amount * float(current_price)
        original_value = transaction.amount * price
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
    aggregate_asset(transaction_objects)
