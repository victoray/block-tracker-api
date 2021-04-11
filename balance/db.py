from pymongo.collection import Collection

from common.db import client
from settings import DATABASE

db = client[DATABASE]
COLLECTION = "balance"
collection: Collection = db[COLLECTION]
collection.create_index("userId", unique=True)
