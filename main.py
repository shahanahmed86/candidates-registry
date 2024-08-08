from fastapi import FastAPI, status
from sentry_sdk import init

from configs import configs
from database import lifespan
from middleware import add_middlewares

init(
    dsn=configs.SENTRY_DSN,
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)

app = FastAPI(lifespan=lifespan)


# middlewares
add_middlewares(app)


# to check whether the server is healthy or not
@app.get("/healthcheck", status_code=status.HTTP_200_OK)
async def healthy():
    return "I am healthy"


# to test the setry error log
@app.get("/sentry-debug")
async def trigger_error():
    _division_by_zero = 1 / 0
