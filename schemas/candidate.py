from .common import Gender

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class CreateCandidate(BaseModel):
    email: EmailStr = Field(...)
    first_name: str = Field(min_length=3, max_length=50)
    last_name: str = Field(min_length=3, max_length=50)
    gender: Gender
    phone: str = Field(min_length=9, max_length=15)
    current_job: str = Field(min_length=3, max_length=50)
    current_employer: str = Field(min_length=3, max_length=50)
    applied_for: str = Field(min_length=3, max_length=50)

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "email": "candidate@domain.com",
                "first_name": "candidate-first-name",
                "last_name": "candidate-last-name",
                "gender": "male",
                "phone": "+923331234567",
                "current_job": "MERN Stack Developer",
                "current_employer": "Agilelan Ltd",
                "applied_for": "FastAPI Backend Developer",
            }
        },
    )
