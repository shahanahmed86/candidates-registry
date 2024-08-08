from passlib.context import CryptContext

from configs import configs

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(value: str) -> str:
    return bcrypt_context.hash(configs.BCRYPT_SALT, value)


def verify(hashed_value: str, value: str) -> bool:
    return bcrypt_context.verify(configs.BCRYPT_SALT, hashed_value, value)
