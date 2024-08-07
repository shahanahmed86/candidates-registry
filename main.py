from fastapi import FastAPI
from starlette import status

app = FastAPI()


@app.get("/healthcheck", status_code=status.HTTP_200_OK)
def healthy():
    return "I am healthy"
