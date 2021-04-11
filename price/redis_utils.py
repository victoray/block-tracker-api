import logging
import sys

import redis

from settings import REDIS_URL


def redis_connect() -> redis.client.Redis:
    try:
        client = redis.Redis.from_url(REDIS_URL)
        ping = client.ping()
        if ping is True:
            return client
    except redis.AuthenticationError:
        logging.error("Authentication Error")
        sys.exit(1)


redis_client = redis_connect()
