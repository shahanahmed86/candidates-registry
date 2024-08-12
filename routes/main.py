from os import uname

from fastapi import APIRouter, status

router = APIRouter()


# to check whether the server is healthy or not
@router.get("/healthcheck", status_code=status.HTTP_200_OK)
async def healthy():
    return f"I am healthy at {uname().nodename}"


# to test the setry error log
@router.get("/sentry-debug")
async def trigger_error():
    _division_by_zero = 1 / 0
