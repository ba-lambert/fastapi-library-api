import uuid

from sqlalchemy import DateTime
from pydantic import BaseModel


class BorrowBookSchema(BaseModel):
    book_id: uuid.UUID
    user_id: uuid.UUID
    quantity: int
    borrowed_at: DateTime