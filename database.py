import os
import json
from cryptography.fernet import Fernet
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///bot.db")
# Для твоего тарифа Railway, DATABASE_URL должен быть PostgreSQL, но если его нет, возьмется SQLite
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# Генерируем ключ шифрования (или берем из переменной)
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY", Fernet.generate_key().decode())
cipher = Fernet(ENCRYPTION_KEY.encode())

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    telegram_id = Column(String, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Progress(Base):
    __tablename__ = "progress"
    id = Column(Integer, primary_key=True)
    telegram_id = Column(String)
    current_stage = Column(String, default="diagnostic") # diagnostic, level1...
    current_step = Column(Integer, default=0) # какой вопрос задан последним
    encrypted_answers = Column(Text, default="{}") # Зашифрованный JSON с ответами

def init_db():
    Base.metadata.create_all(bind=engine)
    print("✅ База данных инициализирована.")

def encrypt_data(data):
    return cipher.encrypt(json.dumps(data).encode()).decode()

def decrypt_data(encrypted_str):
    return json.loads(cipher.decrypt(encrypted_str.encode()).decode())