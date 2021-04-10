from fastapi import APIRouter
from starlette.background import BackgroundTasks

from balance.db import collection
from balance.models import Balance
from common.utils import calculate_balance

router = APIRouter(prefix="/balance")


@router.get("/", response_model=Balance)
async def get_balance(background_tasks: BackgroundTasks):
    balance = collection.find_one({})
    background_tasks.add_task(calculate_balance)
    return Balance.parse_obj(balance) if balance else Balance()
