from passlib.context import CryptContext

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(value: str) -> str:
    return bcrypt_context.hash(value)


def verify(hashed_value: str, value: str) -> bool:
    return bcrypt_context.verify(hashed_value, value)
