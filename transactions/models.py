from datetime import datetime
from enum import IntEnum
from typing import Optional

from bson import ObjectId

from common.models import Ownable
from transactions.db import collection


class Transaction(Ownable):
    class Type(IntEnum):
        ADD = 0
        REMOVE = 1

    type: Type
    date: datetime
    price: float
    amount: float
    assetId: str
    pnl: Optional[float]
    pnlPercent: Optional[float]
    coin: Optional[dict]
    id: Optional[str]
    _id: Optional[ObjectId]

    def save(self):
        collection.update_one(
            {"_id": ObjectId(self.id)},
            {"$set": self.dict(include={"pnl", "pnlPercent", "amount"})},
        )
