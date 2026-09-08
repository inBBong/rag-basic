"""
상품 테이블에 접근하는 곳입니다.

DB 를 다루는 코드는 전부 여기 모읍니다.
Service 나 API 에서 db.query(...) 를 직접 쓰지 않습니다.
"""

from datetime import datetime, timedelta

from sqlalchemy import desc, func

from app.models.product import Product


def find_all(db, limit=20):
    return db.query(Product).limit(limit).all()


def find_by_category(db, category, limit=20):
    return db.query(Product).filter(Product.category == category).limit(limit).all()


# 제품 아이디로 해당 제품정보 반환 함수
def find_by_id(db, product_id):
    return db.query(Product).filter(Product.product_id == product_id).first()


# 최근에 등록된 상품을 최신순으로 찾습니다.
#   created_at 이 비어 있는 상품(CSV 로 처음 적재한 100개)은 신상품이 아니므로 걸러냅니다.
#   days 를 주면 "최근 7일 안에 등록된 것" 처럼 기간까지 좁힙니다. 없으면 전체 기간에서 봅니다.
def find_recent(db, limit=5, days=None):
    query = db.query(Product).filter(Product.created_at.isnot(None))

    if days:
        query = query.filter(Product.created_at >= datetime.now() - timedelta(days=days))

    return query.order_by(desc(Product.created_at)).limit(limit).all()


# 최근에 등록된 상품을 "비싼 순" 으로 찾습니다.
#   find_recent 와 걸러내는 조건(created_at 이 있는 신상품만, 기간)은 똑같고
#   줄 세우는 기준만 created_at -> price 로 다릅니다.
#   같은 가격이면 더 최근에 등록된 것을 앞에 둡니다.
def find_recent_expensive(db, limit=3, days=None):
    query = db.query(Product).filter(Product.created_at.isnot(None))

    if days:
        query = query.filter(Product.created_at >= datetime.now() - timedelta(days=days))

    return query.order_by(desc(Product.price), desc(Product.created_at)).limit(limit).all()


# 한 카테고리의 가격 통계를 한 줄로 냅니다.
#   "이 신상품이 비싸다" 를 그냥 말하면 근거가 없습니다.
#   같은 카테고리의 평균/최저/최고가와 나란히 놓아야 얼마나 비싼지 말할 수 있습니다.
#   .first() 가 돌려주는 Row 는 stats.avg_price 처럼 label 이름으로 꺼내 씁니다.
def get_category_price_stats(db, category):
    return (
        db.query(
            func.count(Product.product_id).label("count"),
            func.avg(Product.price).label("avg_price"),
            func.min(Product.price).label("min_price"),
            func.max(Product.price).label("max_price"),
        )
        .filter(Product.category == category)
        .first()
    )


# 같은 카테고리에서 기준 가격보다 싼 상품을 비싼 순으로 찾습니다.
#   "이게 제일 비싸요" 로 끝내지 않고 "부담되면 이 정도 대안이 있어요" 까지 붙이려고 씁니다.
#   price < max_price 조건이 기준이 된 상품 자신도 같이 걸러줍니다.
def find_cheaper_in_category(db, category, max_price, limit=3):
    return (
        db.query(Product)
        .filter(Product.category == category, Product.price < max_price)
        .order_by(desc(Product.price))
        .limit(limit)
        .all()
    )


# 클라이언트로부터 제품정보를 받아서 DB에 저장하는 함수
def save(db, product):
    db.add(product)
    db.commit()
    return product