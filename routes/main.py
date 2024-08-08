from fastapi import APIRouter, status
from sentry_sdk import init

from configs import configs

router = APIRouter()

init(
    dsn=configs.SENTRY_DSN,
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)


# to check whether the server is healthy or not
@router.get("/healthcheck", status_code=status.HTTP_200_OK)
async def healthy():
    return "I am healthy"


# to test the setry error log
@router.get("/sentry-debug")
async def trigger_error():
    _division_by_zero = 1 / 0
