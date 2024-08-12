import pytest
from fastapi import Response
from motor.motor_asyncio import AsyncIOMotorDatabase

from .constants import insert_candidate, signup_data, update_candidate
from .utils import client, create_test_candidate, db, remove_test_candidate


@pytest.mark.asyncio
async def test_create_candidate(db: AsyncIOMotorDatabase):
    try:
        client.post("/user", json=signup_data)

        response: Response = client.post("/candidates", json=insert_candidate)
        res_data = response.json()

        assert response.status_code == 201
        assert res_data["message"] == "You've successfully created a candidate"

        response: Response = client.post("/candidates", json=insert_candidate)
        res_data = response.json()

        assert response.status_code == 409
        assert res_data["detail"] == "The user has already registered with this email!"
    finally:
        await remove_test_candidate(db)


@pytest.mark.asyncio
async def test_get_candidate(db: AsyncIOMotorDatabase):
    try:
        candidate = create_test_candidate(db)

        response: Response = client.get("/candidates/66ba31a06eb3581a6e0dc3f3")
        res_data = response.json()

        assert response.status_code == 404
        assert res_data["detail"] == "Candidate not found!"

        response: Response = client.get("/candidates/invalid_object_id")
        res_data = response.json()

        assert response.status_code == 400
        assert res_data["detail"] == "The ID was invalid!"

        response: Response = client.get(f"/candidates/{candidate['id']}")
        res_data = response.json()

        assert response.status_code == 200
        assert res_data["message"] == "You've successfully found the candidate!"
    finally:
        await remove_test_candidate(db)


@pytest.mark.asyncio
async def test_update_candidate(db: AsyncIOMotorDatabase):
    try:
        candidate = create_test_candidate(db)

        response: Response = client.get("/candidates/66ba31a06eb3581a6e0dc3f3")
        res_data = response.json()

        assert response.status_code == 404
        assert res_data["detail"] == "Candidate not found!"

        response: Response = client.get("/candidates/invalid_object_id")
        res_data = response.json()

        assert response.status_code == 400
        assert res_data["detail"] == "The ID was invalid!"

        response: Response = client.put(
            f"/candidates/{candidate['id']}", json=update_candidate
        )
        res_data = response.json()

        assert response.status_code == 200
        assert res_data["message"] == "You have successfully updated the candidate"

    finally:
        await remove_test_candidate(db)


@pytest.mark.asyncio
async def test_delete_candidate(db: AsyncIOMotorDatabase):
    try:
        candidate = create_test_candidate(db)

        response: Response = client.get("/candidates/66ba31a06eb3581a6e0dc3f3")
        res_data = response.json()

        assert response.status_code == 404
        assert res_data["detail"] == "Candidate not found!"

        response: Response = client.get("/candidates/invalid_object_id")
        res_data = response.json()

        assert response.status_code == 400
        assert res_data["detail"] == "The ID was invalid!"

        response: Response = client.delete(f"/candidates/{candidate['id']}")
        res_data = response.json()

        assert response.status_code == 200
        assert res_data["message"] == "You've successfully deleted the candidate!"
    finally:
        await remove_test_candidate(db)


@pytest.mark.asyncio
async def test_get_all_candidate(db: AsyncIOMotorDatabase):
    try:
        create_test_candidate(db)

        response: Response = client.get(
            "/candidates", params={"skip": 1, "limit": 10, "search": "can"}
        )
        res_data = response.json()

        assert response.status_code == 200
        assert res_data["message"] == "You've successfully get all the categories"
        assert "counts" in res_data["data"]
        assert "pages" in res_data["data"]
        assert "page" in res_data["data"]

        response: Response = client.get(
            "/candidates", params={"skip": 0, "limit": 10, "search": "can"}
        )
        res_data = response.json()

        assert response.status_code == 422
    finally:
        await remove_test_candidate(db)
