from typing import Annotated

from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClient

from database import get_db

db_dependency = Annotated[AsyncIOMotorClient, Depends(get_db)]
