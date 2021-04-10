from pydantic.main import BaseModel


class Asset(BaseModel):
    ID = "id"
    NAME = "name"
    PRICE = "price"
    AMOUNT = "amount"

    id: str
    name: str
    price: str
    amount: float
    coin: dict
