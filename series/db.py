from pymongo.collection import Collection

from common.db import client
from settings import DATABASE

db = client[DATABASE]
SERIES_COLLECTION = "series"
collection: Collection = db[SERIES_COLLECTION]
collection.create_index([("date", -1)])
