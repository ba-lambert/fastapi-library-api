import uuid

from sqlalchemy import Column, String, ForeignKey, Date
from sqlalchemy.dialects.postgresql import UUID as PGUUID

from app.models.base import Base


class BookModel(Base):
    __tablename__ = 'T_BOK_BOOK'
    BOK_ID = Column(PGUUID(as_uuid=True), default=uuid.uuid4, nullable=False, unique=True, primary_key=True, index=True)
    BOK_TITLE = Column(String, index=True, nullable=False)
    BOK_DESCRIPTION = Column(String(2000), index=True, nullable=False)
    BOK_AUTHOR = Column(String, index=True, nullable=False)
    BOK_ISBN = Column(String, unique=True, index=True, nullable=False)
    BOK_PUBLISHED_YEAR = Column(String, nullable=True)
    BOK_COVER_URL = Column(String, nullable=True)
    BOK_PUBLISHER = Column(String, nullable=True)
    BOK_USER_ID = Column(PGUUID(as_uuid=True), ForeignKey('T_USR_USER.id', ondelete='CASCADE'), nullable=False, index=True)
