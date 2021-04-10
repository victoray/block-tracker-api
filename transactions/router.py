from bson import ObjectId
from fastapi import APIRouter, HTTPException
from starlette.background import BackgroundTasks

from transactions.db import collection
from transactions.models import Transaction
from transactions.utils import get_transaction_objects

router = APIRouter(prefix="/transactions")


@router.get("/")
async def get_transactions(asset_id: str):
    docs = collection.find({"assetId": asset_id})
    transactions = get_transaction_objects(docs)

    return transactions


@router.post("/")
async def create_transaction(body: Transaction):
    transaction = body.dict(exclude_none=True)
    if transaction.get("type") == Transaction.Type.REMOVE:
        transaction.update({"amount": transaction.get("amount") * -1})

    result = collection.insert_one(transaction)
    # background_tasks.add_task(aggregate_transactions, {"assetId": body.assetId})
    return {"id": str(result.inserted_id)}


@router.put("/{transaction_id}/")
async def update_transaction(
    transaction_id: str, body: dict, background_tasks: BackgroundTasks
):
    result = collection.update_one({"_id": ObjectId(transaction_id)}, {"$set": body})

    if not result.matched_count:
        raise HTTPException(status_code=404)

    # background_tasks.add_task(aggregate_transactions, {"assetId": body.get("assetId")})
    return {"id": transaction_id}


@router.delete("/{transaction_id}")
async def delete_transaction(transaction_id: str, background_tasks: BackgroundTasks):
    result = collection.delete_one({"_id": ObjectId(transaction_id)})

    if not result.deleted_count:
        raise HTTPException(status_code=404)

    # background_tasks.add_task(aggregate_transactions)
    return ""
