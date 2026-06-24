class Config:
    SQLALCHEMY_DATABASE_URI = \
        "sqlite:///trekking.sqlite3"

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = "secret-key"

    JWT_SECRET_KEY = "jwt-secret"