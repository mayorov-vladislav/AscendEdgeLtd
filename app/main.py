from fastapi import FastAPI
from app.api.v1 import leads, sales

app = FastAPI(title="AscendEdgeLtd API")

app.include_router(leads.router, prefix="/api/v1/leads", tags=["leads"])
app.include_router(sales.router, prefix="/api/v1/sales", tags=["sales"])


@app.get("/")
async def root():
    return {"message": "AscendEdgeLtd API is running"}