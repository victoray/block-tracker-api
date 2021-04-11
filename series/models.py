from datetime import datetime
from typing import Optional

from pydantic.fields import Field

from common.models import Ownable


class Series(Ownable):
    id: Optional[str]
    date: datetime = Field(default_factory=datetime.now)
    balance: float
