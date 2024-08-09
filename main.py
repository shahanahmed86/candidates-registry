from fastapi import Depends, FastAPI

from middleware.auth import verify_session
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
    dependencies=[Depends(verify_session)],
)
