from datetime import datetime, timedelta, timezone

from fastapi import Response
from jwt import decode, encode

from configs import configs


def jwt_encode(
    user_id: str,
    res: Response,
    expires_delta=timedelta(milliseconds=int(configs.JWT_EXPIRY)),
) -> str:
    encoded = {"sub": "candidates", "id": user_id}
    expires = datetime.now(timezone.utc) + expires_delta
    encoded.update({"exp": expires})

    token = encode(encoded, key=configs.JWT_SECRET, algorithm=configs.JWT_ALGORITHM)
    res.set_cookie(key="access_token", value=token, httponly=True)


def jwt_decode(token: str) -> dict:
    return decode(token, key=configs.JWT_SECRET, algorithms=[configs.JWT_ALGORITHM])
