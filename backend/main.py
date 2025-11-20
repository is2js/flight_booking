from contextlib import asynccontextmanager

from fastapi import FastAPI

from backend.crud.database import init_db
from backend.routers import users, flights


# init_db()를 lifespan으로 변경
@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield
    # 필요하면 종료 로직 추가


app = FastAPI(lifespan=lifespan)

app.include_router(users.router)
app.include_router(flights.router)


@app.get("/", tags=["Root"])
def hello():
    return {"message": "Hello, World!"}
