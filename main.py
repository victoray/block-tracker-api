import json

import firebase_admin
import uvicorn
from fastapi import FastAPI, Depends
from firebase_admin import credentials
from starlette.middleware.cors import CORSMiddleware

from assets.router import router as asset_router
from auth.dependencies import get_current_user
from balance.router import router as balance_router
from price.router import router as price_router
from settings import FIREBASE_APP
from transactions.router import router as transaction_router


def initialize():
    """set credentials (intermediate credential file is created)"""
    credentials_path = "credentials.json"
    cred = credentials.Certificate(credentials_path)
    try:
        firebase_admin.get_app(FIREBASE_APP)
    except ValueError:
        firebase_admin.initialize_app(cred, name=FIREBASE_APP)


initialize()


app = FastAPI(
    title="Block Tracker API",
    version="1.0.0",
    dependencies=[Depends(get_current_user)],
)


origins = [
    "http://localhost",
]

app.include_router(asset_router)
app.include_router(transaction_router)
app.include_router(price_router)
app.include_router(balance_router)
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
