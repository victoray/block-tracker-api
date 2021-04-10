import json

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware

from routers import assets, transactions, price

app = FastAPI(title="Block Tracker API", version="1.0.0")

origins = [
    "http://localhost",
]

app.include_router(assets.router)
app.include_router(transactions.router)
app.include_router(price.router)
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


class Balance(BaseModel):
    amount: float = 0
    change: float = 0


@app.get("/balance/", response_model=Balance)
async def balance():
    return Balance()


@app.get("/coin-list/")
async def get_coin_list():
    return coin_list


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
