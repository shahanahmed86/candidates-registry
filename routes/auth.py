from fastapi import APIRouter, Body, HTTPException, Response, status

from database import db_dependency
from helper import format_response
from library.bcrypt import hash
from library.jwt import jwt_encode
from middleware.auth import guest_session, user_session
from models.user import User
from schemas.user import AuthResponse, GuestResponse, Login, Signup

router = APIRouter()


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_description="Logging in",
    response_model_by_alias=False,
    response_model=AuthResponse,
    responses={
        401: format_response("Not Authorized!"),
        403: format_response("You need to login before proceed!"),
    },
)
async def logged_in(user: User = user_session):
    return {
        "message": "You have an active logged-in session",
        "data": user,
    }


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_description="Create a new User to login",
    response_model_by_alias=False,
    response_model=AuthResponse,
    responses={
        403: format_response("You need to logout before proceed!"),
        409: format_response("Email address already exists!"),
    },
)
async def signup(
    db: db_dependency, res: Response, _=guest_session, data: Signup = Body(...)
):
    coll = db.get_collection("users")

    exists = await coll.find_one({"email": data.email})
    if exists:
        raise HTTPException(status.HTTP_409_CONFLICT, "Email address already exists!")

    data.password = hash(data.password)
    new_user = await coll.insert_one(
        data.model_dump(),
    )

    user_id = new_user.inserted_id
    user = await coll.find_one({"_id": user_id})

    jwt_encode(str(user["_id"]), res)

    return {
        "message": "Account was created and logged in successfully",
        "data": user,
    }


@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    response_description="Logging in",
    response_model_by_alias=False,
    response_model=AuthResponse,
    responses={
        403: format_response("You need to logout before proceed!"),
        409: format_response("Email address already exists!"),
    },
)
async def login(
    db: db_dependency, res: Response, _=guest_session, data: Login = Body(...)
):
    coll = db.get_collection("users")

    user = await coll.find_one({"email": data.email})
    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Not Authorized!")

    jwt_encode(str(user["_id"]), res)

    return {"message": "You've logged in successfully", "data": user}


@router.delete(
    "/logout",
    status_code=status.HTTP_200_OK,
    response_description="Logging out",
    response_model_by_alias=False,
    response_model=GuestResponse,
    responses={
        401: format_response("Not Authorized!"),
        403: format_response("You need to login before proceed!"),
    },
)
async def logout(res: Response, _=user_session):
    res.delete_cookie(key="access_token", httponly=True)
    return {"message": "You've successfully logged out"}
