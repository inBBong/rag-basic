"""
청크 테이블

긴 글을 통째로 검색하면 엉뚱한 부분까지 딸려옵니다.
그래서 의미 단위로 잘라서 한 조각씩 저장합니다. 이 조각을 청크라고 부릅니다.

여기에 들어오는 것은 두 종류입니다.
  product  상품 상세 문서를 ## 섹션 단위로 자른 것
  review   고객 후기 한 건
"""

from sqlalchemy import Column, ForeignKey, Integer, String, Text

from app.db import Base


class Chunk(Base):
    __tablename__ = "chunks"

    chunk_id = Column(Integer, primary_key=True)

    # 이 청크가 어디서 왔는지
    source = Column(String)  # "product" 또는 "review"
    source_id = Column(String)  # P001 또는 R0001
    product_id = Column(String, ForeignKey("products.product_id"))
    section = Column(String)  # 상품이면 "주요 성분" 같은 섹션 제목, 후기면 비어 있음

    # 실제로 검색 대상이 되는 글입니다.
    content = Column(Text)

    # content 를 숫자 1536개로 바꾼 것입니다. 이걸로 뜻이 비슷한 글을 찾습니다.
    # SQLite 에는 벡터 타입이 없어서 JSON 문자열로 저장합니다.
    # 마지막에 이 한 줄만 Vector(1536) 으로 바꾸면 Supabase 로 넘어갑니다.
    embedding = Column(Text)