from flask import Flask
from backend.config import Config
from backend.models import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    return app