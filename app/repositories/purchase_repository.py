# 구매 이력 테이블에 접근하는 곳입니다.

from sqlalchemy import desc, func

from app.models.product import Product
from app.models.purchase import Purchase


# 고객의 구매 내역을 최근 순으로 찾습니다.
def find_by_customer(db, customer_id, limit=20):
    return (
        db.query(Purchase, Product)
        .join(Product, Product.product_id == Purchase.product_id)
        .filter(Purchase.customer_id == customer_id)
        .order_by(Purchase.purchased_at.desc())
        .limit(limit)
        .all()
    )

# 많이 팔린 상품을 순서대로 찾습니다.
def find_best_selling(db, limit=5):
    sold = func.sum(Purchase.quantity).label("sold")
    return (
        db.query(Product, sold)
        .join(Purchase, Purchase.product_id == Product.product_id)
        .group_by(Product.product_id)
        .order_by(desc("sold"))
        .limit(limit)
        .all()
    )