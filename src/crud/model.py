"""
Este módulo contiene la clase de repositorio para las operaciones CRUD
del modelo VehicleModelModel.
"""

import typing as t
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert

from models.model import VehicleModelModel
from schemas.model import VehicleModelCreateSchema, VehicleModelUpdateSchema


class CRUDModel:
    def __init__(self, model: type[VehicleModelModel]):
        self.model = model

    @staticmethod
    def get_all_filtered(
        db: Session,
        *,
        greater: t.Optional[float] = None,
        lower: t.Optional[float] = None,
    ) -> t.List[VehicleModelModel]:
        query = db.query(VehicleModelModel)
        if greater is not None:
            query = query.filter(VehicleModelModel.average_price > greater)
        if lower is not None:
            query = query.filter(VehicleModelModel.average_price < lower)
        return query.all()

    @staticmethod
    def get_by_id(db: Session, model_id: int) -> t.Optional[VehicleModelModel]:
        return (
            db.query(VehicleModelModel).filter(VehicleModelModel.id == model_id).first()
        )

    @staticmethod
    def get_by_name(db: Session, name: str) -> t.Optional[VehicleModelModel]:
        return (
            db.query(VehicleModelModel).filter(VehicleModelModel.name == name).first()
        )

    @staticmethod
    def create(db: Session, model: VehicleModelCreateSchema) -> VehicleModelModel:
        db_model = VehicleModelModel(**model.model_dump())
        db.add(db_model)
        db.commit()
        db.refresh(db_model)
        return db_model

    @staticmethod
    def update(
        db: Session,
        db_model: VehicleModelModel,
        model_in: t.Union[VehicleModelUpdateSchema, t.Dict[str, t.Any]],
    ) -> VehicleModelModel:
        if isinstance(model_in, dict):
            update_data = model_in
        else:
            update_data = model_in.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(db_model, key, value)

        db.add(db_model)
        db.commit()
        db.refresh(db_model)
        return db_model

    @staticmethod
    def delete(db: Session, model_id: int) -> t.Optional[VehicleModelModel]:
        db_model = CRUDModel.get_by_id(db, model_id)
        if db_model:
            db.delete(db_model)
            db.commit()
        return db_model

    def bulk_insert(self, db: Session, *, models_data: list[VehicleModelCreateSchema]):
        """
        Inserta múltiples modelos en la base de datos.
        """
        if not models_data:
            return

        models_dict = [model.model_dump() for model in models_data]
        stmt = insert(self.model).values(models_dict)
        stmt = stmt.on_conflict_do_nothing(index_elements=["name"])
        db.execute(stmt)
        db.commit()
