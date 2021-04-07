from pymongo.collection import Collection

from db.base import client
from settings import DATABASE

db = client[DATABASE]
COLLECTION = "assets"
collection: Collection = db[COLLECTION]
collection.create_index("id", unique=True)
