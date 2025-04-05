import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Полный абсолютный путь к папке проекта
PROJECT_DIR = Path(__file__).parent.parent  # Поднимаемся на уровень выше app/
INSTANCE_DIR = PROJECT_DIR / 'instance'
INSTANCE_DIR.mkdir(exist_ok=True)  # Создаем папку если не существует

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY') or 'dev-key-123'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.expanduser('~/myapp/water_delivery/instance/delivery.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOGIN_VIEW = 'auth.login'
