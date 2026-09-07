"""
상품 관련 HTTP 엔드포인트입니다.

여기서는 요청을 받아서 Service 에 넘기고, 결과를 돌려주기만 합니다.
DB 를 직접 만지지 않습니다.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import get_db
from app.schemas.product import ProductOut
from app.services import product_service

router = APIRouter()


@router.get("/products", response_model=list[ProductOut])
def get_products(category: str | None = None, limit: int = 20, db: Session = Depends(get_db)):
    return product_service.get_products(db, category, limit)