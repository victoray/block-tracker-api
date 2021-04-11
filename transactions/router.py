from bson import ObjectId
from fastapi import APIRouter, HTTPException, Depends
from starlette.background import BackgroundTasks

from auth.dependencies import get_current_active_user
from common.utils import update_assets
from mail.send_email import send_email
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
async def create_transaction(
    body: Transaction,
    background_tasks: BackgroundTasks,
    user=Depends(get_current_active_user),
):
    transaction = body.dict(exclude_none=True)
    transaction.update(userId=user.uid)
    if transaction.get("type") == Transaction.Type.REMOVE:
        transaction.update({"amount": transaction.get("amount") * -1})

    result = collection.insert_one(transaction)

    background_tasks.add_task(
        send_email,
        user.uid,
        "Transaction created",
        f"""Token: {body.assetId}
            Amount: {body.amount}
        """,
    )
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


@router.delete("/{transaction_id}/")
async def delete_transaction(
    transaction_id: str,
    background_tasks: BackgroundTasks,
    user=Depends(get_current_active_user),
):
    query = {"_id": ObjectId(transaction_id), "userId": user.uid}
    result = collection.find_one_and_delete(query)

    if not result:
        raise HTTPException(status_code=404)

    transaction = Transaction.parse_obj(result)
    background_tasks.add_task(update_assets, transaction, user.uid)
    background_tasks.add_task(
        send_email,
        user.uid,
        "Transaction Deleted",
        f"""
        Token: {transaction.assetId}
        Amount: {transaction.amount}
        """,
    )

    return ""
