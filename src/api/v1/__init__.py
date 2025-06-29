from fastapi import APIRouter

from api.v1.brands import router as brands_router
from api.v1.models import router as models_router

router = APIRouter(prefix="/v1")
router.include_router(brands_router)
router.include_router(models_router)
