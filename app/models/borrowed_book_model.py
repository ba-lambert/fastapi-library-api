import uuid

from sqlalchemy import Column, ForeignKey, DateTime, func, Integer
from sqlalchemy.dialects.postgresql import UUID as PGUUID

from app.models.base import Base


class BorrowBookModel(Base):
    __tablename__ = 'T_BOR_BORROWED_BOOK'

    BOR_ID = Column(PGUUID(as_uuid=True), primary_key=True, index=True, unique=True, nullable=False, default=uuid.uuid4)
    BOR_BOOK_ID = Column(PGUUID(as_uuid=True),ForeignKey('T_BOK_BOOK.BOK_ID',ondelete="CASCADE") ,nullable=False, index=True)
    BOR_USER_ID = Column(PGUUID(as_uuid=True),ForeignKey('T_USR_USER.id',ondelete="CASCADE") ,nullable=False, index=True)
    BOR_QUANTITY = Column(Integer, nullable=False)
    BOR_BORROWED_AT = Column(DateTime(timezone=True),server_default=func.now(), nullable=False)
    BOR_RETURNED_AT = Column(DateTime(timezone=True), nullable=True)
    BOR_CREATED_AT = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    BOR_UPDATED_AT = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)