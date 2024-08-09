from typing import Annotated, Optional

from fastapi import Depends, HTTPException, Request, status

from bson import ObjectId
from database import db_dependency
from library.jwt import jwt_decode
from models.user import User


async def verify_session(db: db_dependency, req: Request):
    token = req.cookies.get("access_token")

    if not token:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN, "You need to login before proceed"
        )

    payload = jwt_decode(token)
    user_id: Optional[str] = payload.get("id")

    if user_id is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Not Authorized")

    coll = db.get_collection("users")

    user = await coll.find_one({"_id": ObjectId(user_id)})
    return user


user_session = Annotated[User, Depends(verify_session)]


async def verify_guest(req: Request):
    token = req.cookies.get("access_token")
    if token:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN, "You need to logout before proceed"
        )


guest_session = Annotated[None, Depends(verify_guest)]
