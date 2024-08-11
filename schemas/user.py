from pydantic import BaseModel, ConfigDict, EmailStr, Field

from models.user import User

from .common import Gender


class Signup(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(min_length=6, max_length=20)
    first_name: str | None = Field(None, min_length=3, max_length=50)
    last_name: str | None = Field(None, min_length=3, max_length=50)
    gender: Gender
    phone: str | None = Field(None, min_length=9, max_length=15)

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "email": "test@domain.com",
                "password": "123Abc456",
                "first_name": "shahan",
                "last_name": "khan",
                "gender": "male",
                "phone": "+923331234567",
            }
        },
    )


class Login(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...)

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "email": "test@domain.com",
                "password": "123Abc456",
            }
        },
    )


class AuthResponse(BaseModel):
    message: str
    data: User


class GuestResponse(BaseModel):
    message: str
