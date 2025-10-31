from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.db import get_app_db
from app.schemas.borrow_book_schema import BorrowBookSchema
from app.services.borrow_book_service import BorrowBookService

borrow_book_router = APIRouter(tags=["borrow"])
borrow_book_service = BorrowBookService()


@borrow_book_router.post("")
def borrow_book(borrow_data: BorrowBookSchema, db: Session = Depends(get_app_db), current_user=Depends()):
    return borrow_book_service.borrow_book(db, borrow_data, current_user)
