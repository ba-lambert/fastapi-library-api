import uuid

from pydantic import BaseModel

class StockCreateSchema(BaseModel):
    book_id: uuid.UUID
    quantity: int

class StockResponseSchema(BaseModel):
    id: uuid.UUID
    book_id: uuid.UUID
    quantity: int
    available_quantity: bool
    created_at: str
    updated_at: str
