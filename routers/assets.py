import json
from typing import List

from fastapi import APIRouter
from pydantic import BaseModel

from db.assets import collection as asset_collection
from db.transactions import collection as transaction_collection
from routers.transactions import Transaction

router = APIRouter(prefix="/assets")


class Asset(BaseModel):
    ID = "id"
    NAME = "name"
    PRICE = "price"
    AMOUNT = "amount"

    id: str
    name: str
    price: str
    amount: float
    coin: dict


with open("coinlist.json") as f:
    coin_list: dict = json.load(f)


def aggregate_asset(transactions: List[Transaction]):
    groups: dict = {}
    for transaction in transactions:
        groups[transaction.assetId] = groups.get(transaction.assetId, []) + [
            transaction
        ]

    assets = []

    for asset, transactions in groups.items():
        asset = Asset(
            id=asset,
            name=coin_list.get("Data", {}).get(asset, {}).get("CoinName"),
            coin=coin_list.get("Data", {}).get(asset, {}),
            price=2000,
            amount=sum(map(lambda x: x.amount, transactions)),
        )
        assets.append(asset.dict())

    for asset in assets:
        asset_collection.update_one(
            {"id": asset.get("id")}, {"$set": asset}, upsert=True
        )


@router.get("/", response_model=List[Asset])
async def get_assets():
    transactions = transaction_collection.find({})
    aggregate_asset([Transaction.parse_obj(t) for t in transactions])
    result = asset_collection.find({})
    assets = []
    for doc in result:
        assets.append(Asset.parse_obj(doc))

    return assets


@router.get("/{asset_id}", response_model=Asset)
async def get_asset(asset_id: str):

    return {"asset_id": asset_id}


@router.put("/{asset_id}", response_model=Asset)
async def update_asset(asset_id: str):
    return {"asset_id": asset_id}


@router.delete("/{asset_id}")
async def delete_asset(asset_id: str):
    return {"asset_id": asset_id}
