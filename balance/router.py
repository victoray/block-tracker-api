from fastapi import APIRouter, Depends
from starlette.background import BackgroundTasks

from auth.dependencies import get_current_active_user
from balance.db import collection
from balance.models import Balance
from common.utils import calculate_balance

router = APIRouter(prefix="/balance")


@router.get("/", response_model=Balance)
async def get_balance(
    background_tasks: BackgroundTasks, user=Depends(get_current_active_user)
):
    balance = collection.find_one({})
    background_tasks.add_task(calculate_balance, user.uid)
    return Balance.parse_obj(balance) if balance else Balance(userId=user.uid)
