from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database.db import get_app_db
from app.enums.role_enum import RoleEnum
from app.schemas.book_schema import BookCreateSchema
from app.services.book_service import BookService
from app.utils.security_utils import SecurityUtils

book_router = APIRouter(tags=['books'])
book_service = BookService()
security_utils = SecurityUtils()


@book_router.get('/{id}')
def get_book_by_id(id: UUID, db: Session = Depends(get_app_db)):
    return book_service.get_book_by_id(db, id)


@book_router.get('/')
def get_all_books(db: Session = Depends(get_app_db),
                  offset: int = Query(0, ge=0, description="Number of items to skip"),
                  limit: int = Query(10, ge=1, le=100, description="Number of items to return")
                  ):
    return book_service.get_all_books(db, skip=offset, limit=limit)

@book_router.post("/")
def create_book(
    book_data: BookCreateSchema,
    db: Session = Depends(get_app_db),
    current_user = Depends(security_utils.role_required([RoleEnum.LIBRARIAN]))
):
    return book_service.create_book(db=db, book_data=book_data, current_user=current_user)