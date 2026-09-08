# 구매 이력 테이블에 접근하는 곳입니다.

from sqlalchemy import desc, func

from app.models.product import Product
from app.models.purchase import Purchase


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