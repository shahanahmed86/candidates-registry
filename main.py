from fastapi import FastAPI

from middleware import add_middlewares
from routes import auth, main

app = FastAPI()


# middlewares
add_middlewares(app)

app.include_router(router=main.router)
app.include_router(prefix="/user", tags=["user"], router=auth.router)
