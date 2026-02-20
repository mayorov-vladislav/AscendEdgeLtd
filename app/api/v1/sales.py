from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_sales():
    return {"message": "Sales endpoint works"}