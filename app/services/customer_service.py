"""고객 관련 업무 로직입니다."""

from app.repositories import customer_repository


# 구매액이 큰 고객을 딕셔너리 목록으로 돌려줍니다.
def get_top_spenders(db, limit=5):
    rows = customer_repository.find_top_spenders(db, limit)
    return [
        {
            "customer_id": customer.customer_id,
            "name": customer.name,
            "city": customer.city,
            "phone": customer.phone,
            "email": customer.email,
            "total_spend": total_spend,
        }
        for customer, total_spend in rows
    ]


# 피부 타입별 고객 수를 딕셔너리 목록으로 돌려줍니다.
def count_by_skin_type(db):
    rows = customer_repository.count_by_skin_type(db)
    return [{"skin_type": skin_type, "count": count} for skin_type, count in rows]


def get_customers(db, skin_type=None, limit=20):
    if skin_type:
        return customer_repository.find_by_skin_type(db, skin_type, limit)
    return customer_repository.find_all(db, limit)