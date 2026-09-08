# 상품 테이블에 접근하는 곳입니다.

from app.models.product import Product


def find_all(db, limit=20):
    return db.query(Product).limit(limit).all()


def find_by_category(db, category, limit=20):
    return db.query(Product).filter(Product.category == category).limit(limit).all()


def find_by_id(db, product_id):
    return db.query(Product).filter(Product.product_id == product_id).first()


def save(db, product):
    db.add(product)
    db.commit()
    return product