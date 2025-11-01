from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.models.book_model import BookModel
from app.models.borrowed_book_model import BorrowBookModel
from app.models.stock_model import StockModel
from app.schemas.borrow_book_schema import BorrowBookSchema


class BorrowBookService:
    @staticmethod
    def borrow_book(db: Session, data: BorrowBookSchema, current_user):
        existing_book = db.query(BookModel).filter(BookModel.BOK_ID == data.book_id).first()
        if not existing_book:
            raise HTTPException(status_code=404, detail="Book not found")

        stock = db.query(StockModel).filter(
            and_(
                StockModel.STK_BOOK_ID == data.book_id,
                StockModel.STK_QUANTITY >= data.quantity
            )
        ).first()

        if not stock:
            raise HTTPException(status_code=400, detail="Not enough books in stock")

        borrow_book = BorrowBookModel(
            BOR_BOOK_ID=data.book_id,
            BOR_USER_ID=current_user.id,
            BOR_QUANTITY=data.quantity
        )
        db.add(borrow_book)

        stock.STK_QUANTITY -= data.quantity
        db.commit()
        db.refresh(borrow_book)
        db.refresh(stock)

        return borrow_book
