from bson import ObjectId
from fastapi import HTTPException, status
from motor.motor_asyncio import AsyncIOMotorCollection


def format_response(message: str) -> str:
    return {
        "description": message,
        "content": {"application/json": {"example": {"detail": message}}},
    }


async def check_validaty_and_existance(coll: AsyncIOMotorCollection, _id: str) -> dict:
    if not ObjectId.is_valid(_id):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "The ID was invalid!")

    record = await coll.find_one({"_id": ObjectId(_id)})
    if not record:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Candidate not found!")

    return record
