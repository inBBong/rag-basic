"""
상품 관련 HTTP 엔드포인트입니다.

여기서는 요청을 받아서 Service 에 넘기고, 결과를 돌려주기만 합니다.
DB 를 직접 만지지 않습니다.
"""


from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.schemas.product import ProductCreate, ProductCreatedOut, ProductNewOut, ProductOut
from app.services import product_service

router = APIRouter()


@router.get("/products", response_model=list[ProductOut])
def get_products(category: str | None = None, limit: int = 20, db: Session = Depends(get_db)):
    return product_service.get_products(db, category, limit)


# 최근 등록된 신상품 목록입니다. 챗봇을 거치지 않고 바로 확인할 때 씁니다.
# days 를 주면 "최근 7일" 처럼 기간을 좁힙니다. 안 주면 등록된 신상품 전체에서 최신순으로 봅니다.
@router.get("/products/new", response_model=list[ProductNewOut])
def get_new_products(limit: int = 5, days: int | None = None, db: Session = Depends(get_db)):
    return product_service.get_new_products(db, limit, days)


@router.post("/products", response_model=ProductCreatedOut, status_code=201)
def create_product(request: ProductCreate, db: Session = Depends(get_db)):
    result = product_service.create_product(db, request)
    if result is None:
        raise HTTPException(status_code=409, detail="이미 있는 상품 번호입니다.")
    return result