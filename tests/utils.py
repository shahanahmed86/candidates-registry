import pytest
from fastapi.testclient import TestClient
from motor.motor_asyncio import AsyncIOMotorClient

from database import get_db
from main import app

from .constants import insert_candidate, signup_data

client = TestClient(app, base_url="http://localhost:7000")


@pytest.fixture
def db():
    for database in get_db():
        yield database


async def remove_test_user(db_instance: AsyncIOMotorClient):
    client.delete("/user/logout")

    coll = db_instance.get_collection("users")
    await coll.find_one_and_delete({"email": signup_data["email"]})


def create_test_user():
    client.post("/user", json=signup_data)
    client.delete("/user/logout")


async def remove_test_candidate(db_instance: AsyncIOMotorClient):
    await remove_test_user(db_instance)

    coll = db_instance.get_collection("candidates")
    await coll.find_one_and_delete({"email": insert_candidate["email"]})


def create_test_candidate(db_instance: AsyncIOMotorClient):
    client.post("/user", json=signup_data)

    response = client.post("/candidates", json=insert_candidate)
    return response.json()["data"]
