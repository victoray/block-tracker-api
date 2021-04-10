from typing import Optional

from pydantic.main import BaseModel


class Price(BaseModel):
    priceUSD: Optional[str]
    symbol: str
    slug: str
    name: str
