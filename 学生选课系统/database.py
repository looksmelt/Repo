# app/database.py
from motor.motor_asyncio import AsyncIOMotorClient
from app.settings import get_settings  # 假设你有一个配置模块

settings = get_settings()

client = AsyncIOMotorClient(settings.mongo_uri)
database = client[settings.database_name]

def get_database() -> AsyncIOMotorDatabase:
    return database