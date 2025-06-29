from fastapi import APIRouter
from starlette.responses import Response

router = APIRouter(prefix="/health-check", tags=["Health"])


@router.get("/", status_code=204)
async def health() -> Response:
    # TODO: Add health check for the database
    return Response(status_code=204)
