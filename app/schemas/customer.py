"""고객을 JSON 으로 내보낼 때의 형식입니다."""

from datetime import date

from pydantic import BaseModel


class CustomerOut(BaseModel):
    customer_id: str
    name: str
    gender: str
    age: int
    skin_type: str
    phone: str
    email: str
    city: str
    joined_at: date

    # SQLAlchemy 객체를 그대로 받아서 변환하도록 켜 줍니다.
    model_config = {"from_attributes": True}


# 고객의 구매 내역 한 건입니다. 상품 이름과 가격을 같이 담습니다.
class PurchaseOut(BaseModel):
    purchase_id: str
    product_id: str
    product_name: str
    price: int
    quantity: int
    purchased_at: date



# 고객이 쓴 후기 한 건입니다.
class ReviewOut(BaseModel):
    review_id: str
    product_id: str
    product_name: str
    rating: int
    content: str
    written_at: date


    
# 고객 한 명의 상세 정보입니다.
class CustomerDetailOut(BaseModel):
    customer: CustomerOut
    masked: CustomerOut
    purchases: list[PurchaseOut]
    reviews: list[ReviewOut]
    # 구매 내역에서 계산합니다. 고객 테이블에는 이런 컬럼이 없습니다.
    total_spend: int