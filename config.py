import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # 🔐 Core Security
    SECRET_KEY = os.getenv("SECRET_KEY", "fallback_dev_key")
    
    # 🚀 Development Settings
    DEBUG = True
    TEMPLATES_AUTO_RELOAD = True

    # 🧠 Database (CodeSpace Module)
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "3306")
    DB_NAME = os.getenv("DB_NAME")

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 🛂 IAM Module
    SEED_ROLES = os.getenv("SEED_ROLES", "true").lower() == "true"
    ENABLE_OAUTH = os.getenv("ENABLE_OAUTH", "false").lower() == "true"

    # 📦 Future Modules
    # Add tags like EVALUATION_ENGINE, ML_GLYPH_ENGINE, etc.
