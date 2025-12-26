from flask import Flask
from flask_cors import CORS
from .config import DevelopmentConfig
from .extensions import db, migrate
from . import models

def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)

    CORS(app)

    db.init_app(app)
    migrate.init_app(app, db)

    from .routes.example import example_bp
    from .routes.room import rooms_bp
    app.register_blueprint(example_bp, url_prefix="/api")
    app.register_blueprint(rooms_bp, url_prefix="/api")

    return app
