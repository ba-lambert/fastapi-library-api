from fastapi import FastAPI

from app.routes.book_routes import book_router
from app.routes.user_routes import user_router

app = FastAPI()

app.include_router(user_router, prefix="/user", tags=["user"])
app.include_router(book_router, prefix="/books", tags=["books"])