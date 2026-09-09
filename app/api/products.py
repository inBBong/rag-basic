# 상품 관련 HTTP 엔드포인트입니다.

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.schemas.product import (
    ProductCreate,
    ProductCreatedOut,
    ProductDetailOut,
    ProductNewOut,
    ProductOut,
)
from app.services import product_service

router = APIRouter()


@router.get("/products", response_model=list[ProductOut])
def get_products(category: str = None, limit: int = 20, db: Session = Depends(get_db)):
    return product_service.get_products(db, category, limit)


# 최근 등록된 신상품 목록입니다. 챗봇을 거치지 않고 바로 확인할 때 씁니다.
#
# 이 줄이 아래 /products/{product_id} 보다 **위에** 있어야 합니다.
# FastAPI 는 위에서부터 차례로 맞춰 보기 때문에, 순서를 바꾸면
# "new" 를 상품 번호로 읽어서 404 가 납니다. 고정된 주소를 먼저 씁니다.
@router.get("/products/new", response_model=list[ProductNewOut])
def get_new_products(limit: int = 5, days: int = None, db: Session = Depends(get_db)):
    return product_service.get_new_products(db, limit, days)


@router.get("/products/{product_id}", response_model=ProductDetailOut)
def get_product_detail(product_id: str, db: Session = Depends(get_db)):
    detail = product_service.get_product_detail(db, product_id)

    if detail is None:
        raise HTTPException(status_code=404, detail="그런 상품 번호가 없습니다.")

    return detail


@router.post("/products", response_model=ProductCreatedOut, status_code=201)
def create_product(request: ProductCreate, db: Session = Depends(get_db)):
    result = product_service.create_product(db, request)

    if result is None:
        raise HTTPException(status_code=409, detail="이미 있는 상품 번호입니다.")

    return result