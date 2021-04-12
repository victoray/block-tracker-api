import json
import logging

import firebase_admin
import uvicorn
from fastapi import FastAPI, Depends, APIRouter
from firebase_admin import credentials
from starlette.middleware.cors import CORSMiddleware

from app_settings.router import settings_router
from assets.router import router as asset_router
from auth.dependencies import get_current_user
from balance.router import router as balance_router
from price.router import router as price_router
from series.router import series_router
from settings import FIREBASE_APP, GOOGLE_CREDENTIALS
from transactions.router import router as transaction_router
from worker.celery_app import aggregate_series


def initialize():
    """set credentials (intermediate credential file is created)"""

    cred = credentials.Certificate(json.loads(GOOGLE_CREDENTIALS))
    try:
        firebase_admin.get_app(FIREBASE_APP)
    except ValueError:
        firebase_admin.initialize_app(cred, name=FIREBASE_APP)


initialize()


app = FastAPI(
    title="Block Tracker API",
    version="1.0.0",
)

authenticated_router = APIRouter(dependencies=[Depends(get_current_user)])

log = logging.getLogger(__name__)


@app.on_event("startup")
def init_app():
    aggregate_series.delay()


origins = [
    "http://localhost",
]

authenticated_router.include_router(asset_router)
authenticated_router.include_router(transaction_router)
authenticated_router.include_router(price_router)
authenticated_router.include_router(balance_router)
authenticated_router.include_router(series_router)
authenticated_router.include_router(settings_router)
app.include_router(authenticated_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

with open("coinlist.json") as f:
    coin_list = json.load(f)


@app.get("/")
async def root():
    return {"version": app.version}


@app.get("/coin-list/")
async def get_coin_list():
    return coin_list


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
