from typing import Annotated

from pydantic import BaseModel, BeforeValidator, EmailStr, Field

from schemas.common import Gender

PyObjectId = Annotated[str, BeforeValidator(str)]


class Candidate(BaseModel):
    id: PyObjectId = Field(alias="_id")
    email: EmailStr
    first_name: str
    last_name: str
    gender: Gender
    phone: str
    current_job: str
    current_employer: str
    applied_for: str
