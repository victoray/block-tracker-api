from pymongo.collection import Collection

from common.db import client
from settings import DATABASE

db = client[DATABASE]
BALANCE_COLLECTION = "balance"
collection: Collection = db[BALANCE_COLLECTION]
collection.create_index([("userId", 1), ("assetId", 1)], unique=True)
