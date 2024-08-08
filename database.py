from motor.motor_asyncio import AsyncIOMotorClient

from configs import configs


def get_db():
    url = f"mongodb://{configs.DB_USER}:{configs.DB_PASSWORD}@{configs.DB_HOST}:{configs.DB_PORT}/"
    mongodb_client = AsyncIOMotorClient(url)
    try:
        db = mongodb_client.get_database(configs.DB_NAME)
        yield db
    finally:
        mongodb_client.close()
