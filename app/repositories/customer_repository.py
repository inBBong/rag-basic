"""
고객 테이블에 접근하는 곳입니다.

DB 를 다루는 코드는 전부 여기 모읍니다.
Service 나 API 에서 db.query(...) 를 직접 쓰지 않습니다.
"""

from sqlalchemy import desc, func
from app.models.customer import Customer
from app.models.product import Product
from app.models.purchase import Purchase


def find_all(db, limit=20):
    return db.query(Customer).limit(limit).all()


def find_by_skin_type(db, skin_type, limit=20):
    return db.query(Customer).filter(Customer.skin_type == skin_type).limit(limit).all()


# 구매 금액이 큰 고객을 순서대로 찾습니다.
def find_top_spenders(db, limit=5):
    total_spend = func.sum(Product.price * Purchase.quantity).label("total_spend")
    return (
        db.query(Customer, total_spend)
        .join(Purchase, Purchase.customer_id == Customer.customer_id)
        .join(Product, Product.product_id == Purchase.product_id)
        .group_by(Customer.customer_id)
        .order_by(desc("total_spend"))
        .limit(limit)
        .all()
    )


# 피부 타입별로 고객이 몇 명인지 셉니다.
def count_by_skin_type(db):
    count = func.count(Customer.customer_id).label("count")
    return (
        db.query(Customer.skin_type, count)
        .group_by(Customer.skin_type)
        .order_by(desc("count"))
        .all()
    )