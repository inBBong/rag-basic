"""
상품 테이블에 접근하는 곳입니다.

DB 를 다루는 코드는 전부 여기 모읍니다.
Service 나 API 에서 db.query(...) 를 직접 쓰지 않습니다.
"""

from app.models.product import Product


def find_all(db, limit=20):
    return db.query(Product).limit(limit).all()


def find_by_category(db, category, limit=20):
    return db.query(Product).filter(Product.category == category).limit(limit).all()