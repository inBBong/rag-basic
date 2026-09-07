"""
상품 관련 업무 로직입니다.

지금은 Repository 를 그대로 부르기만 해서 얇아 보입니다.
하지만 나중에 "상품을 저장하고, 상세를 자르고, 임베딩해서 벡터로 저장한다" 처럼
여러 단계를 묶는 자리가 바로 여기입니다.
"""

from app.repositories import product_repository


def get_products(db, category=None, limit=20):
    if category:
        return product_repository.find_by_category(db, category, limit)
    return product_repository.find_all(db, limit)