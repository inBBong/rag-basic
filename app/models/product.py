"""
상품 테이블

정형 데이터와 비정형 데이터가 한 테이블에 같이 있습니다.

정형  : price, category, skin_type ... → SQL 로 조회
비정형: description, detail          → 청킹하고 임베딩해서 검색
"""

from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Text

from app.db import Base


class Product(Base):
    __tablename__ = "products"

    product_id = Column(String, primary_key=True)
    name = Column(String)
    brand = Column(String)
    category = Column(String)
    price = Column(Integer)
    volume = Column(String)
    skin_type = Column(String)
    ingredient = Column(String)
    concern = Column(String)
    tags = Column(String)

    # 짧은 소개글 (3~4문장). 자를 게 없어서 청킹하지 않습니다.
    description = Column(Text)

    # 긴 상세 문서 (평균 1370자, ## 로 나뉜 9개 섹션). RAG 의 주력 재료입니다.
    detail = Column(Text)

    # 등록 시각입니다. POST /products 로 새로 등록하면 자동으로 지금 시각이 찍힙니다.
    # CSV 로 처음 적재한 상품은 비어 있습니다(NULL). 그래서 "값이 있다 = 신상품" 이 됩니다.
    created_at = Column(DateTime, default=datetime.now)