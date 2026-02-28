from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db.base import Base
from app.db.session import engine
from app.api.v1 import leads, sales


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield


app = FastAPI(
    title="AscendEdgeLtd API",
    lifespan=lifespan
)

app.include_router(leads.router, prefix="/api/v1", tags=["leads"])
app.include_router(sales.router, prefix="/api/v1", tags=["sales"])


@app.get("/")
async def root():
    return {"message": "AscendEdgeLtd API is running"}