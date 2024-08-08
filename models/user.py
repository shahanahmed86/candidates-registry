from enum import Enum

from pydantic import BaseModel, Field


class Gender(str, Enum):
    male = "male"
    female = "female"


class User(BaseModel):
    id: str = Field(alias="_id", default=None)
    email: str
    password: str = Field(min_length=6, max_length=20)
    first_name: str = Field(min_length=3, max_length=50)
    last_name: str = Field(min_length=3, max_length=50)
    gender: Gender
    phone: str = Field(min_length=9, max_length=15)

    model_config = {
        "arbitrary_types_allowed": True,
        "json_schema_extra": {
            "example": {
                "email": "test@domain.com",
                "password": "123Abc456",
                "first_name": "shahan",
                "last_name": "khan",
                "gender": "male",
                "phone": "+923362122588",
            }
        },
    }
