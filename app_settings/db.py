from pymongo.collection import Collection

from common.db import client
from settings import DATABASE

db = client[DATABASE]
SERIES_COLLECTION = "app_settings"
settings_collection: Collection = db[SERIES_COLLECTION]
settings_collection.create_index("userId", unique=True)
