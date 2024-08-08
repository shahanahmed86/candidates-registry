from fastapi import APIRouter, status

from helper import db_dependency
from models.user import User

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=User)
async def create_user(db: db_dependency, user: User):
    collection = db.get_collection("users")
    new_user = await collection.insert_one(user.model_dump())
    created_user = await collection.find_one({"_id": new_user.inserted_id})
    return created_user
