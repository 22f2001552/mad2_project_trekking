from datetime import timedelta



class Config:
    SQLALCHEMY_DATABASE_URI = \
        "sqlite:///trekking.sqlite3"

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = "secret-key"

    JWT_SECRET_KEY = "jwt-secret"

    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)

    CACHE_TYPE = "RedisCache"
    
    CACHE_REDIS_HOST = "127.0.0.1"

    CACHE_REDIS_PORT = 6379

    CACHE_DEFAULT_TIMEOUT = 300