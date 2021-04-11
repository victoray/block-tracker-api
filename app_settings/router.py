from fastapi import APIRouter, Depends

from app_settings.db import settings_collection
from app_settings.models import Settings
from auth.dependencies import get_current_active_user

settings_router = APIRouter()


@settings_router.get("/settings/", response_model=Settings)
def get_settings(
    user=Depends(get_current_active_user),
):
    result = settings_collection.find_one(
        {
            "userId": user.uid,
        }
    )
    if result:
        return Settings.parse_obj(result)

    return Settings(userId=user.uid)


@settings_router.post("/settings/", response_model=Settings)
def get_settings(body: dict, user=Depends(get_current_active_user)):
    result = settings_collection.find_one_and_update(
        {
            "userId": user.uid,
        },
        {"$set": body},
        upsert=True,
        return_document=True,
    )

    return Settings.parse_obj(result)
