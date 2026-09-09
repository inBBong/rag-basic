# 후기 테이블에 접근하는 곳입니다.

from app.models.customer import Customer
from app.models.product import Product
from app.models.review import Review


# 고객이 쓴 후기를 최근 순으로 찾습니다.
def find_by_customer(db, customer_id, limit=20):
    return (
        db.query(Review, Product)
        .join(Product, Product.product_id == Review.product_id)
        .filter(Review.customer_id == customer_id)
        .order_by(Review.written_at.desc())
        .limit(limit)
        .all()
    )