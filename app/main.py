from fastapi import FastAPI

from app.routes.book_routes import book_router
from app.routes.borrow_book_route import borrow_book_router
from app.routes.stock_routes import stock_router
from app.routes.user_routes import user_router
from app.utils.book_scheduler import scheduler

app = FastAPI()


@app.on_event("startup")
def startup_event():
    scheduler
    print("Application has started")


app.include_router(user_router, prefix="/user", tags=["user"])
app.include_router(book_router, prefix="/books", tags=["books"])
app.include_router(stock_router, prefix="/stock", tags=["stock"])
app.include_router(borrow_book_router, prefix="/borrow", tags=["borrow"])