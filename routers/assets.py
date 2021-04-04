from typing import List

from fastapi import APIRouter
from pydantic import BaseModel

from db.assets import collection

router = APIRouter(prefix="/assets")


class Asset(BaseModel):
    id: str
    name: str
    price: str
    amount: float
    assetId: str


@router.get("/", response_model=List[Asset])
async def get_assets():
    result = collection.find({})
    assets = []
    for doc in result:
        Asset.parse_obj(doc)

    return assets


@router.post("/")
async def create_asset(asset_id: str):
    return {"asset_id": asset_id}


@router.get("/{asset_id}", response_model=Asset)
async def get_asset(asset_id: str):
    return {"asset_id": asset_id}


@router.put("/{asset_id}", response_model=Asset)
async def update_asset(asset_id: str):
    return {"asset_id": asset_id}


@router.delete("/{asset_id}")
async def delete_asset(asset_id: str):
    return {"asset_id": asset_id}
