"""구매 이력 테이블 (정형 데이터)"""

from sqlalchemy import Column, Date, ForeignKey, Integer, String

from app.db import Base


class Purchase(Base):
    __tablename__ = "purchases"

    purchase_id = Column(String, primary_key=True)
    customer_id = Column(String, ForeignKey("customers.customer_id"))
    product_id = Column(String, ForeignKey("products.product_id"))
    purchased_at = Column(Date)
    quantity = Column(Integer)