from bson import ObjectId
from fastapi import APIRouter, HTTPException

from transactions.db import collection
from transactions.models import Transaction

router = APIRouter(prefix="/transactions")


@router.get("/")
async def get_transactions(asset_id: str):
    docs = collection.find({"assetId": asset_id})
    transactions = []

    for doc in docs:
        transactions.append(Transaction.parse_obj(doc))

    return transactions


@router.post("/")
async def create_transaction(body: Transaction):
    result = collection.insert_one(body.dict(exclude_none=True))
    return {"id": str(result.inserted_id)}


@router.put("/{transaction_id}")
async def update_transaction(transaction_id: str, body: Transaction):
    result = collection.update_one(
        {Transaction.ID: ObjectId(transaction_id)}, body.dict(exclude_none=True)
    )

    if not result.upserted_id:
        raise HTTPException(status_code=404)

    return {"id": transaction_id}


@router.delete("/{transaction_id}")
async def delete_transaction(transaction_id: str):
    result = collection.delete_one({Transaction.ID: ObjectId(transaction_id)})

    if not result.deleted_count:
        raise HTTPException(status_code=404)

    return ""
