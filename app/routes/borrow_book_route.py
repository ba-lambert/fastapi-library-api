from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.db import get_app_db
from app.schemas.borrow_book_schema import BorrowBookSchema
from app.services.borrow_book_service import BorrowBookService
from app.utils.security_utils import SecurityUtils

borrow_book_router = APIRouter(tags=["borrow"])
borrow_book_service = BorrowBookService()
security_util = SecurityUtils()


@borrow_book_router.post('')
def borrow_book(borrow_data: BorrowBookSchema, db: Session = Depends(get_app_db), current_user=Depends(security_util.get_current_user)):
    return borrow_book_service.borrow_book(db, borrow_data, current_user)
