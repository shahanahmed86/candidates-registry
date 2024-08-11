from typing import List

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from models.candidate import Candidate

from .common import Gender


class CreateCandidate(BaseModel):
    email: EmailStr = Field(...)
    first_name: str = Field(min_length=3, max_length=50)
    last_name: str = Field(min_length=3, max_length=50)
    gender: Gender = Field(...)
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


class UpdateCandidate(BaseModel):
    email: EmailStr | None
    first_name: str | None = Field(None, min_length=3, max_length=50)
    last_name: str | None = Field(min_length=3, max_length=50)
    gender: Gender | None
    phone: str | None = Field(None, min_length=9, max_length=15)
    current_job: str | None = Field(None, min_length=3, max_length=50)
    current_employer: str | None = Field(None, min_length=3, max_length=50)
    applied_for: str | None = Field(None, min_length=3, max_length=50)

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "email": "candidate-update@domain.com",
                "first_name": "candidate-first-name-update",
                "last_name": "candidate-last-name-update",
                "gender": "female",
                "phone": "+923331234568",
                "current_job": "Gin Backend Developer",
                "current_employer": "Agilelan Ltd",
                "applied_for": "MERN Stack Developer",
            }
        },
    )


class GetCandidateResponse(BaseModel):
    message: str
    data: Candidate | None


class UpdateOrRemoveCandidateResponse(BaseModel):
    message: str


class CreateCandidateResponse(BaseModel):
    message: str
    data: Candidate


class Pagination(BaseModel):
    counts: int
    pages: int
    page: int
    rows: List[Candidate]


class GetAllCandidatesResponse(BaseModel):
    message: str
    data: Pagination
