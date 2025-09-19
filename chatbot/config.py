import os
from dotenv import load_dotenv
import urllib.parse

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev_secret")

    DB_USER = urllib.parse.quote_plus(os.getenv('DB_USER', 'root'))
    db_password = os.getenv('DB_PASSWORD')
    if db_password:
        DB_PASSWORD = urllib.parse.quote_plus(db_password)
        DB_HOST = os.getenv('DB_HOST', 'localhost')
        DB_PORT = os.getenv('DB_PORT', '3306')
        DB_NAME = os.getenv('DB_NAME', 'smartcrop')
        SQLALCHEMY_DATABASE_URI = (
            f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        )
    else:
        # Use SQLite for development if DB_PASSWORD is not set
        SQLALCHEMY_DATABASE_URI = 'sqlite:///chatbot.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
