import uuid
from sqlalchemy import Column, Boolean, DateTime, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from shared.dates import now


class BaseModelMixin:
    """
    Mixin que añade columnas comunes a los modelos.
    """
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=text("gen_random_uuid()"),
        nullable=False
    )
    is_active = Column(Boolean, default=True, server_default=text('true'), nullable=False)
    created_at = Column(DateTime(timezone=True), default=now, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=now, onupdate=now, server_default=func.now(), nullable=False)
