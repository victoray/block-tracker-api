from datetime import datetime
from time import sleep

from celery import Celery
from celery.utils.log import get_task_logger
from pymongo import MongoClient

from balance.db import BALANCE_COLLECTION
from balance.models import Balance
from common.utils import calculate_balance, aggregate_transactions
from series.db import SERIES_COLLECTION
from series.models import Series
from settings import MONGODB_URL, DATABASE

celery_app = Celery(
    "tasks",
    backend="redis://localhost:6379/0",
    broker="amqp://localhost:5672//",
)

celery_app.conf.update(task_track_started=True)

celery_log = get_task_logger(__name__)


@celery_app.task
def aggregate_series():
    celery_log.info("Starting aggregation")
    client = MongoClient(MONGODB_URL)
    db = client[DATABASE]
    balance_collection = db[BALANCE_COLLECTION]
    series_collection = db[SERIES_COLLECTION]
    celery_log.info(f"Datapoints: {series_collection.count_documents({})}")

    while True:
        balances = balance_collection.find({"assetId": None})
        for balance in balances:
            balance = Balance.parse_obj(balance)
            aggregate_transactions({"userId": balance.userId})
            balance = Balance.parse_obj(calculate_balance(balance.userId))

            series = Series(
                userId=balance.userId, balance=balance.amount, date=datetime.utcnow()
            )
            series_collection.insert_one(series.dict())

        celery_log.info("Ending aggregation cycle, sleeping for 60 seconds")
        sleep(60)
