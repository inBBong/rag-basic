"""고객 관련 업무 로직입니다."""

from app.repositories import customer_repository


def get_customers(db, skin_type=None, limit=20):
    if skin_type:
        return customer_repository.find_by_skin_type(db, skin_type, limit)
    return customer_repository.find_all(db, limit)