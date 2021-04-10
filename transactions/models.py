from datetime import datetime
from enum import IntEnum

from pydantic.main import BaseModel


class Transaction(BaseModel):
    ASSET_ID = "assetId"
    ID = "id_"

    class Type(IntEnum):
        ADD = 0
        REMOVE = 1

    type: Type
    date: datetime
    price: float
    amount: float
    assetId: str
