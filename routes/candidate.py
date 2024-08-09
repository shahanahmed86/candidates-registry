from bson import ObjectId
from fastapi import APIRouter, HTTPException, Path, Query, status

from database import db_dependency
from models.candidate import Candidate
from schemas.candidate import CreateCandidate, UpdateCandidate

router = APIRouter()


@router.post(
    "/",
    response_description="Create a candidate",
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
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
        "data": Candidate(**candidate),
    }


@router.get(
    "/{id}",
    response_description="Get candidate by Id",
    status_code=status.HTTP_200_OK,
    response_model_by_alias=False,
)
async def get_candidate(db: db_dependency, id: str = Path()):
    coll = db.get_collection("candidates")

    if not ObjectId.is_valid(id):
        raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE, "The ID was invalid!")

    candidate = await coll.find_one({"_id": ObjectId(id)})

    return {
        "message": "You've successfully found the candidate!",
        "data": Candidate(**candidate) if candidate else None,
    }


@router.put(
    "/{id}",
    response_description="Update candidate by Id",
    status_code=status.HTTP_200_OK,
    response_model_by_alias=False,
)
async def update_candidate(db: db_dependency, data: UpdateCandidate, id: str = Path()):
    coll = db.get_collection("candidates")

    if not ObjectId.is_valid(id):
        raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE, "The ID was invalid!")

    exists = await coll.find_one(
        {"$and": [{"_id": {"$ne": ObjectId(id)}}, {"email": data.email}]}
    )
    if exists:
        raise HTTPException(
            status.HTTP_409_CONFLICT, "The user has already registered with this email!"
        )

    filter = {"_id": ObjectId(id)}
    payload = {"$set": data.model_dump()}
    updated_candidate = await coll.update_one(filter, payload)

    prefix = "successfully" if updated_candidate.modified_count > 0 else "already"
    return {"message": f"You've {prefix} updated the candidate"}


@router.delete(
    "/{id}",
    response_description="Delete candidate by Id",
    status_code=status.HTTP_200_OK,
    response_model_by_alias=False,
)
async def delete_candidate(db: db_dependency, id: str = Path()):
    coll = db.get_collection("candidates")

    if not ObjectId.is_valid(id):
        raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE, "The ID was invalid!")

    candidate = await coll.find_one_and_delete({"_id": ObjectId(id)})

    prefix = "successfully" if candidate else "already"
    return {
        "message": f"You've {prefix} deleted the candidate!",
    }


@router.get(
    "/",
    response_description="Get all candidates",
    status_code=status.HTTP_200_OK,
    response_model_by_alias=False,
)
async def get_all_candidates(
    db: db_dependency,
    skip: int = Query(1, description="Number of documents to skip", ge=1),
    limit: int = Query(10, description="Number of documents to return", le=100),
    search: str | None = Query(None, description="Search query value"),
):
    coll = db.get_collection("candidates")

    search_query = (
        {
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
        if search
        else {}
    )

    cursor = coll.find(search_query).skip((skip - 1) * limit).limit(limit)
    rows = [Candidate(**doc) async for doc in cursor]

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
