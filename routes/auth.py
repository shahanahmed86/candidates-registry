from fastapi import APIRouter, Body, HTTPException, Response, status

from database import db_dependency
from library.bcrypt import hash
from library.jwt import jwt_encode
from middleware.auth import user_session, guest_session
from models.user import User
from schemas.user import Login, Signup

router = APIRouter()


@router.get(
    "/",
    response_description="Logging in",
    status_code=status.HTTP_200_OK,
    response_model_by_alias=False,
)
async def logged_in(user: user_session):
    return {
        "message": "You have an active logged-in session",
        "data": User(**user),
    }


@router.post(
    "/",
    response_description="Create a new User to login",
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def signup(
    _: guest_session, db: db_dependency, res: Response, data: Signup = Body(...)
):
    coll = db.get_collection("users")

    exists = await coll.find_one({"email": data.email})
    if exists:
        raise HTTPException(status.HTTP_409_CONFLICT, "Email address already exists")

    data.password = hash(data.password)
    new_user = await coll.insert_one(
        data.model_dump(),
    )

    user_id = new_user.inserted_id
    user = await coll.find_one({"_id": user_id})

    jwt_encode(str(user["_id"]), res)

    return {
        "message": "Account was created and logged in successfully",
        "data": User(**user),
    }


@router.post(
    "/login",
    response_description="Logging in",
    status_code=status.HTTP_200_OK,
    response_model_by_alias=False,
)
async def login(
    _: guest_session, db: db_dependency, res: Response, data: Login = Body(...)
):
    coll = db.get_collection("users")

    user = await coll.find_one({"email": data.email})
    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Not Authorized!")

    jwt_encode(str(user["_id"]), res)

    return {"message": "You've logged in successfully", "data": User(**user)}


@router.delete(
    "/logout",
    response_description="Logging out",
    status_code=status.HTTP_200_OK,
    response_model_by_alias=False,
)
async def logout(res: Response):
    res.delete_cookie(key="access_token", httponly=True)
    return {"message": "You've successfully logged out"}
