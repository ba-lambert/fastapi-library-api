from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.book_model import BookModel
from app.models.stock_model import StockModel
from app.schemas.stock_schema import StockCreateSchema


class StockService:
    @staticmethod
    def add_to_stock(db: Session, stock_data: StockCreateSchema):
        existing_book = db.query(BookModel).filter(BookModel.BOK_ID == stock_data.book_id).first()
        if not existing_book:
            return HTTPException(status_code=404, detail="Book not found")

        existing_stock = db.query(StockModel).filter(StockModel.STK_BOOK_ID == stock_data.book_id).first()
        if existing_stock:
            existing_stock.STK_QUANTITY += stock_data.quantity
            db.commit()
            db.refresh(existing_stock)
            return existing_stock


        new_stock = StockModel(
            STK_BOOK_ID=stock_data.book_id,
            STK_QUANTITY=stock_data.quantity
        )
        db.add(new_stock)
        db.commit()
        db.refresh(new_stock)
        return new_stock
