from datetime import datetime
from enum import IntEnum

from bson import ObjectId
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from db.transactions import collection

router = APIRouter(prefix="/transactions")


class Transaction(BaseModel):
    ASSET_ID = "assetId"
    ID = "id_"

    class Type(IntEnum):
        ADD = 0
        REMOVE = 1

    type: Type
    date: datetime
    price: float
    amount: float
    assetId: str


@router.get("/")
async def get_transactions(asset_id: str):
    docs = collection.find({Transaction.ASSET_ID: asset_id})
    transactions = []

    for doc in docs:
        transactions.append(Transaction.parse_obj(doc))

    return transactions


@router.post("/")
async def create_transaction(body: Transaction):
    result = collection.insert_one(body.dict(exclude_none=True))

    return {"id": result.inserted_id}


@router.put("/{transaction_id}")
async def update_transaction(transaction_id: str, body: Transaction):
    result = collection.update_one(
        {Transaction.ID: ObjectId(transaction_id)}, body.dict(exclude_none=True)
    )

    if not result.upserted_id:
        raise HTTPException(status_code=404)

    return {"id": result.inserted_id}


@router.delete("/{transaction_id}")
async def delete_transaction(transaction_id: str):
    result = collection.delete_one({Transaction.ID: ObjectId(transaction_id)})

    if not result.deleted_count:
        raise HTTPException(status_code=404)

    return ""
