"""
CSV 파일을 읽어서 SQLite 에 넣습니다.

실행: python -m pipeline.load_data

- products.csv 와 product_details.csv 는 products 테이블 하나로 합칩니다.
- 파생 컬럼은 만들지 않습니다. 구매 합계액 같은 값은 필요할 때 계산합니다.
- 여러 번 실행해도 됩니다. 매번 테이블을 지우고 다시 만듭니다.
"""

import csv
from datetime import date
from pathlib import Path

from app.db import Base, SessionLocal, engine
from app.models.customer import Customer
from app.models.product import Product
from app.models.purchase import Purchase
from app.models.review import Review

DATA = Path(__file__).parent.parent / "data"


def read_csv(name):
    with open(DATA / name, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def make_customer(row):
    return Customer(
        customer_id=row["customer_id"],
        name=row["name"],
        gender=row["gender"],
        age=int(row["age"]),
        skin_type=row["skin_type"],
        phone=row["phone"],
        email=row["email"],
        city=row["city"],
        joined_at=date.fromisoformat(row["joined_at"]),
    )


def make_product(row, detail_of):
    return Product(
        product_id=row["product_id"],
        name=row["name"],
        brand=row["brand"],
        category=row["category"],
        price=int(row["price"]),
        volume=row["volume"],
        skin_type=row["skin_type"],
        ingredient=row["ingredient"],
        concern=row["concern"],
        tags=row["tags"],
        description=row["description"],
        detail=detail_of[row["product_id"]],
    )


def make_purchase(row):
    return Purchase(
        purchase_id=row["purchase_id"],
        customer_id=row["customer_id"],
        product_id=row["product_id"],
        purchased_at=date.fromisoformat(row["purchased_at"]),
        quantity=int(row["quantity"]),
    )


def make_review(row):
    return Review(
        review_id=row["review_id"],
        purchase_id=row["purchase_id"],
        customer_id=row["customer_id"],
        product_id=row["product_id"],
        rating=int(row["rating"]),
        content=row["content"],
        written_at=date.fromisoformat(row["written_at"]),
    )


def print_result(db):
    print("적재 완료")
    print("  customers ", db.query(Customer).count(), "행  (정형)")
    print("  products  ", db.query(Product).count(), "행  (정형 + 비정형)")
    print("  purchases ", db.query(Purchase).count(), "행  (정형)")
    print("  reviews   ", db.query(Review).count(), "행  (비정형)")
    print()

    product = db.query(Product).first()
    print("  상품 예시 :", product.name)
    print("    description", len(product.description), "자  <- 짧은 소개, 청킹 안 함")
    print("    detail     ", len(product.detail), "자  <- 긴 상세, 청킹 대상")
    print()

    review = db.query(Review).first()
    print("  후기 예시 :", review.review_id, "/", review.rating, "점")
    print("   ", review.content)


def main():
    customer_rows = read_csv("customers.csv")
    product_rows = read_csv("products.csv")
    detail_rows = read_csv("product_details.csv")
    purchase_rows = read_csv("purchases.csv")
    review_rows = read_csv("reviews.csv")

    detail_of = {row["product_id"]: row["detail"] for row in detail_rows}

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    db = SessionLocal()
    db.add_all([make_customer(row) for row in customer_rows])
    db.add_all([make_product(row, detail_of) for row in product_rows])
    db.add_all([make_purchase(row) for row in purchase_rows])
    db.add_all([make_review(row) for row in review_rows])
    db.commit()

    print_result(db)
    db.close()


if __name__ == "__main__":
    main()