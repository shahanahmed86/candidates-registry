from csv import DictWriter
from io import StringIO

from fastapi import APIRouter, HTTPException, Path, Query, status
from fastapi.responses import StreamingResponse

from database import db_dependency
from helper import check_validaty_and_existance, format_response
from schemas.candidate import (
    CreateCandidate,
    CreateCandidateResponse,
    GetAllCandidatesResponse,
    GetCandidateResponse,
    UpdateCandidate,
    UpdateOrRemoveCandidateResponse,
)

router = APIRouter()


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_description="Create a candidate",
    response_model_by_alias=False,
    response_model=CreateCandidateResponse,
    responses={
        409: format_response("The user has already registered with this email!"),
    },
)
async def create_candidate(db: db_dependency, data: CreateCandidate):
    coll = db.get_collection("candidates")

    exists = await coll.find_one({"email": data.email})
    if exists:
        raise HTTPException(
            status.HTTP_409_CONFLICT, "The user has already registered with this email!"
        )

    new_candidate = await coll.insert_one(data.model_dump())
    candidate_id = new_candidate.inserted_id

    candidate = await coll.find_one({"_id": candidate_id})

    return {
        "message": "You've successfully created a candidate",
        "data": candidate,
    }


@router.get(
    "/generate-report",
    response_description="Generate candidates data in CSV",
    status_code=status.HTTP_200_OK,
    response_model_by_alias=False,
    responses={
        404: format_response("Candidates data is empty!"),
        200: {
            "description": "CSV file stream",
            "content": {
                "text/csv": {
                    "example": "id,name,age\n1,John Doe,30\n2,Jane Smith,25",
                }
            },
        },
    },
)
async def generate_report(db: db_dependency):
    coll = db.get_collection("candidates")

    cursor = coll.find({})
    data = [doc async for doc in cursor]

    if not data or len(data) == 0:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Candidates data is empty!")

    # Create an in-memory stream for the CSV data
    output = StringIO()
    writer = DictWriter(output, fieldnames=data[0].keys())
    writer.writeheader()
    writer.writerows(data)

    # Set the stream position to the beginning
    output.seek(0)

    # Return the CSV file as a response
    return StreamingResponse(
        output,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=export.csv"},
    )


@router.get(
    "/{id}",
    status_code=status.HTTP_200_OK,
    response_description="Get candidate",
    response_model_by_alias=False,
    response_model=GetCandidateResponse,
    responses={
        404: format_response("Candidate not found!"),
        400: format_response("The ID was invalid!"),
    },
)
async def get_candidate(db: db_dependency, id: str = Path()):
    coll = db.get_collection("candidates")

    candidate = await check_validaty_and_existance(coll, id)

    return {"message": "You've successfully found the candidate!", "data": candidate}


@router.put(
    "/{id}",
    status_code=status.HTTP_200_OK,
    response_description="Update candidate",
    response_model_by_alias=False,
    response_model=UpdateOrRemoveCandidateResponse,
    responses={
        400: format_response("The ID was invalid!"),
        404: format_response("Candidate not found!"),
        409: format_response("The user has already registered with this email!"),
    },
)
async def update_candidate(db: db_dependency, data: UpdateCandidate, id: str = Path()):
    coll = db.get_collection("candidates")

    candidate = await check_validaty_and_existance(coll, id)

    is_duplicate = await coll.find_one(
        {"$and": [{"_id": {"$ne": candidate["_id"]}}, {"email": data.email}]}
    )
    if is_duplicate:
        raise HTTPException(
            status.HTTP_409_CONFLICT, "The user has already registered with this email!"
        )

    await coll.update_one({"_id": candidate["_id"]}, {"$set": data.model_dump()})

    return {"message": "You have successfully updated the candidate"}


@router.delete(
    "/{id}",
    status_code=status.HTTP_200_OK,
    response_description="Delete candidate",
    response_model_by_alias=False,
    response_model=UpdateOrRemoveCandidateResponse,
    responses={
        404: format_response("Candidate not found!"),
        400: format_response("The ID was invalid!"),
    },
)
async def delete_candidate(db: db_dependency, id: str = Path()):
    coll = db.get_collection("candidates")

    candidate = await check_validaty_and_existance(coll, id)

    await coll.find_one_and_delete({"_id": candidate["_id"]})

    return {
        "message": "You've successfully deleted the candidate!",
    }


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_description="Get all candidates",
    response_model_by_alias=False,
    response_model=GetAllCandidatesResponse,
)
async def get_all_candidates(
    db: db_dependency,
    skip: int = Query(1, description="Number of documents to skip", ge=1),
    limit: int = Query(10, description="Number of documents to return", le=100),
    search: str | None = Query(None, description="Search query value"),
):
    coll = db.get_collection("candidates")

    search_query = (
        {}
        if not search
        else {
            "$or": [
                {"email": {"$regex": search, "$options": "i"}},
                {"first_name": {"$regex": search, "$options": "i"}},
                {"last_name": {"$regex": search, "$options": "i"}},
                {"gender": {"$regex": search, "$options": "i"}},
                {"phone": {"$regex": search, "$options": "i"}},
                {"current_job": {"$regex": search, "$options": "i"}},
                {"current_employer": {"$regex": search, "$options": "i"}},
                {"applied_for": {"$regex": search, "$options": "i"}},
            ]
        }
    )

    cursor = coll.find(search_query).skip((skip - 1) * limit).limit(limit)
    rows = [doc async for doc in cursor]

    counts = await coll.count_documents({})

    return {
        "message": "You've successfully get all the categories",
        "data": {
            "counts": counts,
            "pages": counts // limit,
            "page": skip,
            "rows": rows,
        },
    }
