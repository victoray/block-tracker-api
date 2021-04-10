import os

from dotenv import load_dotenv

load_dotenv()

CMC_KEY = os.getenv("CMC_KEY")
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")
REDIS_URL = os.getenv("REDIS_URL")
