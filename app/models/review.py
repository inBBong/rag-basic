"""
후기 테이블 (비정형 데이터)

content 는 사람이 쓴 문장이라 SQL 로는 제대로 찾을 수 없습니다.
그래서 청킹하고 임베딩해서 벡터로 검색합니다.
"""

from sqlalchemy import Column, Date, ForeignKey, Integer, String, Text

from app.db import Base


class Review(Base):
    __tablename__ = "reviews"

    review_id = Column(String, primary_key=True)
    purchase_id = Column(String, ForeignKey("purchases.purchase_id"))
    customer_id = Column(String, ForeignKey("customers.customer_id"))
    product_id = Column(String, ForeignKey("products.product_id"))
    rating = Column(Integer)
    content = Column(Text)
    written_at = Column(Date)