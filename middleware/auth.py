from typing import Optional

from bson import ObjectId
from fastapi import Depends, HTTPException, Request, Response, status
from jwt import ExpiredSignatureError

from database import db_dependency
from library.jwt import jwt_decode


async def verify_session(db: db_dependency, req: Request, res: Response):
    token = req.cookies.get("access_token")

    if not token:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN, "You need to login before proceed!"
        )

    try:
        payload = jwt_decode(token)
        user_id: Optional[str] = payload.get("id")

        if user_id is None or not ObjectId.is_valid(user_id):
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Not Authorized!")

        coll = db.get_collection("users")

        user = await coll.find_one({"_id": ObjectId(user_id)})

        if not user:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Not Authorized!")

        return user
    except HTTPException as e:
        res.delete_cookie(key="access_token", httponly=True)
        raise HTTPException(e.status_code, e.detail)

    except ExpiredSignatureError as _:
        res.delete_cookie(key="access_token", httponly=True)
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Session is expired!")


user_session = Depends(verify_session)


async def verify_guest(req: Request):
    token = req.cookies.get("access_token")
    if token:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN, "You need to logout before proceed!"
        )


guest_session = Depends(verify_guest)
