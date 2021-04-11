from bson import ObjectId
from fastapi import APIRouter, HTTPException, Depends

from auth.dependencies import get_current_active_user
from transactions.db import collection
from transactions.models import Transaction
from transactions.utils import get_transaction_objects

router = APIRouter(prefix="/transactions")


@router.get("/")
async def get_transactions(asset_id: str, user=Depends(get_current_active_user)):
    docs = collection.find({"assetId": asset_id, "userId": user.uid})
    transactions = get_transaction_objects(docs)

    return transactions


@router.post("/")
async def create_transaction(body: Transaction, user=Depends(get_current_active_user)):
    transaction = body.dict(exclude_none=True)
    transaction.update(userId=user.uid)
    if transaction.get("type") == Transaction.Type.REMOVE:
        transaction.update({"amount": transaction.get("amount") * -1})

    result = collection.insert_one(transaction)
    return {"id": str(result.inserted_id)}


@router.put("/{transaction_id}/")
async def update_transaction(
    transaction_id: str, body: dict, user=Depends(get_current_active_user)
):
    result = collection.update_one(
        {"_id": ObjectId(transaction_id), "userId": user.uid}, {"$set": body}
    )

    if not result.matched_count:
        raise HTTPException(status_code=404)

    return {"id": transaction_id}


@router.delete("/{transaction_id}")
async def delete_transaction(
    transaction_id: str, user=Depends(get_current_active_user)
):
    result = collection.delete_one(
        {"_id": ObjectId(transaction_id), "userId": user.uid}
    )

    if not result.deleted_count:
        raise HTTPException(status_code=404)

    return ""
