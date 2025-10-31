import uuid

from sqlalchemy import Column, ForeignKey, Integer, Boolean, DateTime, func
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from app.models.base import Base


class StockModel(Base):
    __tablename__ = 'T_STK_STOCK'
    STK_ID = Column(PGUUID(as_uuid=True), primary_key=True, index=True, unique=True, nullable=False, default=uuid.uuid4)
    STK_BOOK_ID = Column(PGUUID(as_uuid=True), ForeignKey("T_BOK_BOOK.BOK_ID", ondelete="CASCADE"), nullable=False,
                         index=True)
    STK_QUANTITY = Column(Integer, nullable=False)
    STK_AVAILABLE_QUANTITY = Column(Boolean, nullable=False, default=True)
    STK_CREATED_AT = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    STK_UPDATED_AT = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
