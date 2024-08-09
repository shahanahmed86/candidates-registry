from typing import Annotated

from pydantic import BaseModel, BeforeValidator, EmailStr, Field

from schemas.user import Gender

PyObjectId = Annotated[str, BeforeValidator(str)]


class User(BaseModel):
    id: PyObjectId = Field(alias="_id")
    email: EmailStr
    password: str
    first_name: str | None
    last_name: str | None
    gender: Gender
    phone: str
