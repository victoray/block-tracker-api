from typing import List

from fastapi import APIRouter, Depends
from starlette.background import BackgroundTasks

from assets.db import collection as asset_collection
from assets.models import Asset
from auth.dependencies import get_current_active_user
from common.utils import aggregate_transactions
from transactions.db import collection as transaction_collection

router = APIRouter(prefix="/assets")


@router.get("/", response_model=List[Asset])
async def get_assets(
    background_tasks: BackgroundTasks, user=Depends(get_current_active_user)
):
    query = {"userId": user.uid}
    result = asset_collection.find(query)
    assets = []
    for doc in result:
        assets.append(Asset.parse_obj(doc))

    background_tasks.add_task(aggregate_transactions, query)
    return assets


@router.get("/{asset_id}", response_model=Asset)
async def get_asset(asset_id: str):

    return {"asset_id": asset_id}


@router.put("/{asset_id}", response_model=Asset)
async def update_asset(asset_id: str):
    return {"asset_id": asset_id}


@router.delete("/{asset_id}/")
async def delete_asset(asset_id: str, user=Depends(get_current_active_user)):
    transaction_collection.delete_many({"assetId": asset_id, "userId": user.uid})
    asset_collection.delete_one({"id": asset_id, "userId": user.uid})
    return ""
