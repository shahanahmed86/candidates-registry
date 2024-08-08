from fastapi import APIRouter, status
from models.user import User
from helper import db_dependency

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, user: User):
    coll = db.get_collection("users")
    print(coll)
    return [user]
