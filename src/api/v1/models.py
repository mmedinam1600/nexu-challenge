from fastapi import APIRouter

router = APIRouter(prefix="/models", tags=["Models"])


@router.get("/")
async def get_models() -> str:
    return "Models!"
