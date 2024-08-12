from typing import Annotated

from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from configs import configs


def get_db():
    url = f"mongodb://{configs.DB_USER}:{configs.DB_PASSWORD}@{configs.DB_HOST}:{configs.DB_PORT}/{configs.DB_NAME}"
    mongodb_client = AsyncIOMotorClient(url)
    print("Database connected!")
    try:
        db = mongodb_client.get_database()
        yield db
    finally:
        print("Database connection closed!")
        mongodb_client.close()


db_dependency = Annotated[AsyncIOMotorDatabase, Depends(get_db)]
