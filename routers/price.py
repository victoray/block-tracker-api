from fastapi import APIRouter, Depends

from price.coinmarketcap import get_latest_price
from price.models import Price

router = APIRouter(prefix="/price")


async def latest_price(symbol: str):
    return get_latest_price(symbol)


@router.get("/", response_model=Price)
async def get_price(price: dict = Depends(latest_price)):
    return price
