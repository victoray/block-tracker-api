import json
import logging
from typing import Dict

import pydash
from fastapi import HTTPException
from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects

from price import settings
from price.models import Price

# FIAT
from price.redis_utils import redis_client

NGN_ID = "2819"
USD_ID = "2781"

# CRYPTO
BTC_ID = "1"
ETH_ID = "1027"
SUPPORTED_CRYPTO = [BTC_ID, ETH_ID]

# CACHE
CACHE_TIME = 120

CMC_URL = "https://pro-api.coinmarketcap.com"
headers = {
    "Accepts": "application/json",
    "X-CMC_PRO_API_KEY": settings.CMC_KEY,
}
parameters = {"convert_id": f"{USD_ID}"}

session = Session()
session.headers.update(headers)


def get_latest_price(symbol: str) -> Price:
    cached = redis_client.get(symbol)
    if cached:
        print(f"Cache Hit: {symbol}")
        return Price.parse_obj(json.loads(cached))

    try:
        parameters.update({"symbol": symbol})
        response = session.get(
            f"{CMC_URL}/v1/cryptocurrency/quotes/latest",
            params=parameters,
        )

        if not response.ok:
            logging.error(response.text)
            raise HTTPException(status_code=500, detail="Something went wrong")

        response_data: Dict = response.json().get("data", dict())
        symbol = symbol.upper()
        symbol_ = pydash.get(response_data, f"{symbol}.symbol", "").lower()
        slug = pydash.get(response_data, f"{symbol}.slug")
        name = pydash.get(response_data, f"{symbol}.name")
        price_usd = pydash.get(response_data, f"{symbol}.quote.{USD_ID}.price")

        price = Price(
            symbol=symbol_,
            slug=slug,
            name=name,
            priceUSD=price_usd,
        )

        redis_client.setex(symbol, CACHE_TIME, json.dumps(price.dict()))

        return price

    except (ConnectionError, Timeout, TooManyRedirects) as e:
        logging.error(e)
        raise HTTPException(status_code=500, detail="Something went wrong")
