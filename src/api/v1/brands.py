from fastapi import APIRouter

router = APIRouter(prefix="/brands", tags=["Brands"])


@router.get("/")
async def get_brands() -> str:
    return "Brands"
