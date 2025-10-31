# python
from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session

from app.database.db import get_app_db
from app.models.book_model import BookModel
from app.utils.api_request import ApiRequest


def save_book_to_db(db: Session, books_data):
    for book in books_data:
        isbn = book.get('isbn')

        if isbn:
            existing_book = db.query(BookModel).filter(BookModel.BOK_ISBN == isbn).first()
        else:
            existing_book = db.query(BookModel).filter(
                BookModel.BOK_TITLE == book['title'],
                BookModel.BOK_AUTHOR == book['author'],
            ).first()

        if not existing_book:
            db_book = BookModel(
                BOK_TITLE=book['title'],
                BOK_DESCRIPTION=book.get('description', 'No description available'),
                BOK_AUTHOR=book['author'] or 'Unknown Author',
                BOK_ISBN=isbn or 'Unknown',
                BOK_PUBLISHED_YEAR=book.get('published_date') or 'Unknown',
                BOK_COVER_URL=book.get('cover_url') or '',
                BOK_PUBLISHER=book.get('publisher') or 'Unknown Publisher',
                BOK_USER_ID="d62cb205-46f0-4c70-949c-85921c5c8fc2",
            )
            db.add(db_book)
    db.commit()


def schedule_book_saving():
    db_gen = get_app_db()
    db: Session = next(db_gen)
    try:
        books = ApiRequest.fetch_google_books_api(query="programming", max_results=40)
        save_book_to_db(db, books)
    finally:
        try:
            next(db_gen)
        except StopIteration:
            pass


scheduler = BackgroundScheduler()
scheduler.add_job(schedule_book_saving, 'interval', hours=24)
scheduler.start()
