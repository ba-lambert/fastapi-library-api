import uuid

from sqlalchemy import Column, String, Enum, Boolean, DateTime, func
from sqlalchemy.dialects.postgresql import UUID

from app.enums.gender_enum import GenderEnum
from app.enums.role_enum import RoleEnum
from app.models.base import Base


class UserModel(Base):
    __tablename__ = "T_USR_USER"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True, unique=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=True)
    hashed_password = Column(String, nullable=False)
    gender = Column(Enum(GenderEnum), nullable=True)
    role = Column(Enum(RoleEnum), default=RoleEnum.GUEST, nullable=False)
    is_active = Column(Boolean, default=1, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(),onupdate=func.now() , nullable=False)