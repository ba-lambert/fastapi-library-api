from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app.models.book_model import BookModel
from app.schemas.book_schema import BookCreateSchema


class BookService:
    @staticmethod
    def get_book_by_id(db: Session, book_id: UUID):
        db_book = db.query(BookModel).filter(BookModel.BOK_ID == book_id).first()
        if not db_book:
            return HTTPException(status.HTTP_204_NO_CONTENT, detail="Book not found")
        return db_book

    @staticmethod
    def get_all_books(db, skip: int = 0, limit: int = 10):
        books = db.query(BookModel).offset(skip).limit(limit).all()
        return books

    @staticmethod
    def create_book(db: Session, book_data: BookCreateSchema, current_user):
        db_book = db.query(BookModel).filter(BookModel.BOK_TITLE == book_data.title).first()
        if db_book:
            raise HTTPException(status_code=400, detail="Book already exists")
        new_book = BookModel(
            BOK_TITLE=book_data.title,
            BOK_AUTHOR=book_data.author,
            BOK_PUBLISHED_YEAR=book_data.published_year,
            BOK_ISBN=book_data.isbn,
            BOK_DESCRIPTION=book_data.description,
            BOK_COVER_URL=book_data.cover_url,
            BOK_PUBLISHER=book_data.publisher,
            BOK_USER_ID=current_user.id,
        )
        db.add(new_book)
        db.commit()
        db.refresh(new_book)
        return new_book
