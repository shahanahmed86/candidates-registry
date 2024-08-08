from typing import Annotated

from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from database import get_db

db_dependency = Annotated[AsyncIOMotorDatabase, Depends(get_db)]
