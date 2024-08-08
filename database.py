from contextlib import asynccontextmanager

from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

from configs import configs


# method for start the MongoDb Connection
async def startup_db_client(app: FastAPI):
    url = f"mongodb://{configs.DB_USER}:{configs.DB_PASSWORD}@{configs.DB_HOST}:{configs.DB_PORT}/"
    app.mongodb_client = AsyncIOMotorClient(url)
    app.mongodb = app.mongodb_client.get_database(configs.DB_NAME)
    print("MongoDB connected!")


# method to close the database connection
async def shutdown_db_client(app: FastAPI):
    app.mongodb_client.close()
    print("Database disconnected!")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start the database connection
    await startup_db_client(app)
    yield
    # Close the database connection
    await shutdown_db_client(app)
