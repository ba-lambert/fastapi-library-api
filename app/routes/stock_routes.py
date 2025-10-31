from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.db import get_app_db
from app.schemas.stock_schema import StockCreateSchema
from app.services.stock_service import StockService

stock_router = APIRouter(tags=['stock'])
stock_service = StockService()


@stock_router.post('')
def add_to_stock(data: StockCreateSchema, db: Session = Depends(get_app_db)):
    return stock_service.add_to_stock(db, data)
