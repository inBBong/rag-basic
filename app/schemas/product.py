"""
상품을 JSON 으로 내보낼 때의 형식입니다.

DB 모델(Product)을 그대로 내보내지 않고 이 형식을 거칩니다.
어떤 값이 나가는지 한눈에 보이고, 내보내고 싶지 않은 값을 뺄 수 있습니다.

detail 은 평균 1370자라 목록 응답에 넣으면 너무 커집니다. 그래서 뺐습니다.

추후 정부사업 같은 경우는 무조건 Spring + Oracle 형태로 구축이 되는데 (DTO)
"""

from pydantic import BaseModel


class ProductOut(BaseModel):
    product_id: str
    name: str
    brand: str
    category: str
    price: int
    volume: str
    skin_type: str
    ingredient: str
    concern: str
    tags: str
    description: str

    # SQLAlchemy 객체를 그대로 받아서 변환하도록 켜 줍니다.
    model_config = {"from_attributes": True}