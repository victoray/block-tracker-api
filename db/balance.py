from pymongo.collection import Collection

from db.base import client
from settings import DATABASE

db = client[DATABASE]
COLLECTION = "balance"
collection: Collection = db[COLLECTION]
