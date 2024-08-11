from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse

from middleware.auth import user_session
from middleware.main import add_middlewares
from routes import auth, candidate, main

app = FastAPI(
    title="Candidate APIs",
    summary="A sample application doing CRUD operations on candidates",
)

# middlewares
add_middlewares(app)

app.include_router(router=main.router)
app.include_router(prefix="/user", tags=["user"], router=auth.router)
app.include_router(
    prefix="/candidates",
    tags=["candidates"],
    router=candidate.router,
    dependencies=[user_session],
)


@app.exception_handler(HTTPException)
async def http_exception_handler(_, exc: HTTPException):
    res = JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})
    if exc.status_code in {status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN}:
        res.delete_cookie(key="access_token", httponly=True)

    return res
