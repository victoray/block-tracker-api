import os

from dotenv import load_dotenv

load_dotenv()

DATABASE = "BlockTracker"
MONGODB_URL = os.getenv(
    "MONGODB_URL",
    "mongodb+srv://addressStore:PuWYYPhpqXjSgaou@cluster0.rntu3.mongodb.net/<dbname>?retryWrites=true&w=majority",
)
FIREBASE_APP = "BlockTracker"
CMC_KEY = os.getenv("CMC_KEY")
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")
REDIS_URL = os.getenv("REDIS_URL")
MAILGUN_API_KEY = os.getenv("MAILGUN_API_KEY")
