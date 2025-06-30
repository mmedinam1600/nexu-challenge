from typing import List
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from crud.model import CRUDModel
from schemas.model import VehicleModelUpdateSchema
from models.model import VehicleModelModel


class ModelService:
    @staticmethod
    def get_all_models_filtered(
        db: Session,
        *,
        greater: float | None = None,
        lower: float | None = None,
    ) -> List[VehicleModelModel]:
        """Obtiene una lista de todos los modelos, con filtros opcionales por precio."""
        return CRUDModel.get_all_filtered(db, greater=greater, lower=lower)

    @staticmethod
    def update_model_price(
        db: Session, model_id: int, model_schema: VehicleModelUpdateSchema
    ) -> VehicleModelModel:
        """Actualiza el precio de un modelo específico."""
        db_model = CRUDModel.get_by_id(db, model_id=model_id)
        if not db_model:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"El modelo con id '{model_id}' no existe.",
            )

        update_data = model_schema.model_dump(exclude_unset=True)
        return CRUDModel.update(db, db_model=db_model, model_in=update_data)
