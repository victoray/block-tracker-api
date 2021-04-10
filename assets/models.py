from typing import Optional

from pydantic.main import BaseModel


class Asset(BaseModel):
    id: str
    name: str
    price: str
    amount: float
    coin: dict
    pnl: Optional[float]
    pnlPercent: Optional[float]
    currentValue: Optional[float]
    originalValue: Optional[float]
