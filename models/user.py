from typing import Optional
from bson import ObjectId
from pydantic import BaseModel, Field
from enum import Enum


class Gender(str, Enum):
    male = "male"
    female = "female"


class User(BaseModel):
    id: Optional[ObjectId] = Field(alias="_id", default=None)
    email: str
    password: str = Field(min_length=6, max_length=20)
    first_name: str = Field(min_length=3, max_length=50)
    last_name: str = Field(min_length=3, max_length=50)
    gender: Gender
    phone: str = Field(min_length=9, max_length=15)

    model_config = {
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str},
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
