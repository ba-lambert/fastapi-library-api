import uuid

from datetime import datetime as DateTime
from pydantic import BaseModel


class BorrowBookSchema(BaseModel):
    book_id: uuid.UUID
    # user_id: uuid.UUID
    quantity: int
    borrowed_at: DateTime
    will_return_at: DateTime