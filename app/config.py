import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "tatrack-dev-secret-2024")
    _db_url = os.getenv("DATABASE_URL", "sqlite:///tatrack.db")
    if _db_url.startswith("postgres://"):
        _db_url = _db_url.replace("postgres://", "postgresql://", 1)
    SQLALCHEMY_DATABASE_URI = _db_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False
