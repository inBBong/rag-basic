# 상품 관련 HTTP 엔드포인트입니다.

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.schemas.product import ProductCreate, ProductCreatedOut, ProductOut
from app.services import product_service

router = APIRouter()


@router.get("/products", response_model=list[ProductOut])
def get_products(category: str = None, limit: int = 20, db: Session = Depends(get_db)):
    return product_service.get_products(db, category, limit)


@router.post("/products", response_model=ProductCreatedOut, status_code=201)
def create_product(request: ProductCreate, db: Session = Depends(get_db)):
    result = product_service.create_product(db, request)

    if result is None:
        raise HTTPException(status_code=409, detail="이미 있는 상품 번호입니다.")

    return result