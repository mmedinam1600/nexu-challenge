from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import Response

from core.database import get_db

router = APIRouter(prefix="/health-check", tags=["Health"])


@router.get("/", status_code=status.HTTP_204_NO_CONTENT)
async def health(db: Session = Depends(get_db)) -> Response:
    try:
        db.execute(text("SELECT 1"))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Error en la conexión a la base de datos: {e}",
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
