
# config.py
import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev')
    DATABASE_URL = os.getenv('DATABASE_URL')  # e.g. postgresql://user:pass@host:5432/dbname
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'mysql+pymysql://user:pass@localhost/dbname')  # For SQLAlchemy
    WEATHER_API_KEY = os.getenv('WEATHER_API_KEY', '9b7e648c20c9f0034e9d3721d7946901')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
