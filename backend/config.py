import os
from datetime import timedelta

BASE_DIR = os.path.abspath(
    os.path.dirname(__file__)
)


class Config:

    SQLALCHEMY_DATABASE_URI = (
        "sqlite:///" +
        os.path.join(
            BASE_DIR,
            "instance",
            "trekking.sqlite3"
        ).replace("\\", "/")
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = "secret-key"

    JWT_SECRET_KEY = "jwt-secret"

    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)

    CACHE_TYPE = "RedisCache"
    
    CACHE_REDIS_HOST = "localhost"

    CACHE_REDIS_PORT = 6379

    CACHE_DEFAULT_TIMEOUT = 300