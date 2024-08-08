from datetime import datetime, timedelta, timezone

from jwt import decode, encode

from configs import configs


def jwt_encode(
    user_id: int,
    expires_delta=timedelta(milliseconds=int(configs.JWT_EXPIRY)),
) -> str:
    expires = datetime.now(timezone.utc) + expires_delta
    encoded_payload = {"id": user_id, "exp": expires}

    return encode(
        encoded_payload, key=configs.JWT_SECRET, algorithm=configs.JWT_ALGORITHM
    )


def jwt_decode(token: str) -> dict:
    return decode(token, key=configs.JWT_SECRET, algorithms=[configs.JWT_ALGORITHM])
