from typing import Optional

from common.models import Ownable


class Asset(Ownable):
    id: str
    name: str
    price: str
    amount: float
    coin: dict
    pnl: Optional[float]
    pnlPercent: Optional[float]
    currentValue: Optional[float]
    originalValue: Optional[float]
