import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

class Config:
    """Configuration de base (commune à tous les environnements)"""

    # Sécurité
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")

    # Flask
    JSON_SORT_KEYS = False

    # Base de données (par défaut : SQLite)
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        f"sqlite:///{BASE_DIR / 'database.sqlite3'}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False
