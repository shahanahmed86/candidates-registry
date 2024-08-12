import pytest
from fastapi import Response
from motor.motor_asyncio import AsyncIOMotorDatabase

from .constants import login_data, signup_data
from .utils import client, create_test_user, db, remove_test_user


@pytest.mark.asyncio
async def test_logged_in(db: AsyncIOMotorDatabase):
    response: Response = client.get("/user")
    res_data = response.json()

    assert response.status_code == 403
    assert res_data["detail"] == "You need to login before proceed!"

    try:
        client.post("/user", json=signup_data)

        response: Response = client.get("/user")
        res_data = response.json()

        assert response.status_code == 200
        assert res_data["message"] == "You have an active logged-in session"
    finally:
        await remove_test_user(db)


@pytest.mark.asyncio
async def test_signup(db: AsyncIOMotorDatabase):
    try:
        response: Response = client.post("/user", json=signup_data)
        res_data = response.json()

        assert response.status_code == 201
        assert res_data["message"] == "Account was created and logged in successfully"
    finally:
        await remove_test_user(db)


@pytest.mark.asyncio
async def test_login(db: AsyncIOMotorDatabase):
    try:
        create_test_user()
        response: Response = client.post("/user/login", json=login_data)
        res_data = response.json()

        assert response.status_code == 200
        assert res_data["message"] == "You've logged in successfully"
    finally:
        await remove_test_user(db)


@pytest.mark.asyncio
async def test_logout(db: AsyncIOMotorDatabase):
    response: Response = client.delete("/user/logout")
    res_data = response.json()

    assert response.status_code == 403
    assert res_data["detail"] == "You need to login before proceed!"

    try:
        client.post("/user", json=signup_data)

        response: Response = client.delete("/user/logout")
        res_data = response.json()

        assert response.status_code == 200
        assert res_data["message"] == "You've successfully logged out"
    finally:
        await remove_test_user(db)
