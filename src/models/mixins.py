from sqlalchemy import Column, Integer, Boolean, DateTime, text
from sqlalchemy.sql import func
from shared.dates import now


class BaseModelMixin:
    """
    Mixin que añade columnas comunes a los modelos.
    """

    id = Column(Integer, primary_key=True, index=True)
    is_active = Column(
        Boolean, default=True, server_default=text("true"), nullable=False
    )
    created_at = Column(
        DateTime(timezone=True), default=now, server_default=func.now(), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=now,
        onupdate=now,
        server_default=func.now(),
        nullable=False,
    )
