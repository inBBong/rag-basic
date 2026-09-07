"""고객 테이블 (정형 데이터)"""

from sqlalchemy import Column, Date, Integer, String

from app.db import Base


class Customer(Base):
    __tablename__ = "customers"

    customer_id = Column(String, primary_key=True)
    name = Column(String)
    gender = Column(String)
    age = Column(Integer)
    skin_type = Column(String)
    phone = Column(String)
    email = Column(String)
    city = Column(String)
    joined_at = Column(Date)

    # 구매 합계액 같은 파생 컬럼은 두지 않습니다.
    # 실제 회사 DB 에도 그런 컬럼은 없습니다. 필요할 때 구매 이력에서 계산합니다.
    # -> repositories/customer_repository.py 의 find_top_spenders 참고