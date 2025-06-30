from typing import Dict, Any, Union, List
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert

from models.model import VehicleModelModel
from schemas.model import VehicleModelCreateMigrationSchema, VehicleModelUpdateSchema


class CRUDModel:
    def __init__(self, model: type[VehicleModelModel]):
        self.model = model

    @staticmethod
    def get_all_filtered(
        db: Session,
        *,
        greater: float | None = None,
        lower: float | None = None,
    ) -> List[VehicleModelModel]:
        query = db.query(VehicleModelModel)
        if greater is not None:
            query = query.filter(VehicleModelModel.average_price > greater)
        if lower is not None:
            query = query.filter(VehicleModelModel.average_price < lower)
        return query.all()

    @staticmethod
    def get_by_id(db: Session, model_id: int) -> VehicleModelModel | None:
        return (
            db.query(VehicleModelModel).filter(VehicleModelModel.id == model_id).first()
        )

    @staticmethod
    def get_by_name(db: Session, name: str) -> VehicleModelModel | None:
        return (
            db.query(VehicleModelModel).filter(VehicleModelModel.name == name).first()
        )

    @staticmethod
    def create(
        db: Session, model: VehicleModelCreateMigrationSchema
    ) -> VehicleModelModel:
        db_model = VehicleModelModel(**model.model_dump())
        db.add(db_model)
        db.commit()
        db.refresh(db_model)
        return db_model

    @staticmethod
    def update(
        db: Session,
        db_model: VehicleModelModel,
        model_in: Union[VehicleModelUpdateSchema, Dict[str, Any]],
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

    def bulk_insert(
        self, db: Session, *, models_data: list[VehicleModelCreateMigrationSchema]
    ):
        if not models_data:
            return

        models_dict = [model.model_dump() for model in models_data]
        stmt = insert(self.model).values(models_dict)
        stmt = stmt.on_conflict_do_nothing(index_elements=["name"])
        db.execute(stmt)
        db.commit()
