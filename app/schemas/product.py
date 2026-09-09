"""
상품을 JSON 으로 내보낼 때의 형식입니다.

DB 모델(Product)을 그대로 내보내지 않고 이 형식을 거칩니다.
어떤 값이 나가는지 한눈에 보이고, 내보내고 싶지 않은 값을 뺄 수 있습니다.

detail 은 평균 1370자라 목록 응답에 넣으면 너무 커집니다. 그래서 뺐습니다.

추후 정부사업 같은 경우는 무조건 Spring + Oracle 형태로 구축이 되는데 (DTO)
"""

from datetime import datetime

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
    # 등록 시각입니다. CSV 로 처음 적재한 상품은 값이 없어서 None 이 나갑니다.
    created_at: datetime | None = None

    # SQLAlchemy 객체를 그대로 받아서 변환하도록 켜 줍니다.
    model_config = {"from_attributes": True}



# 신상품 목록의 형식입니다.
# ProductOut 을 쓰지 않는 이유는, 서비스가 AI 에게 보낼 만큼만 추려서 돌려주기 때문입니다.
# created_at 은 서비스에서 이미 "2026-09-08" 문자열로 바꿔 놓았습니다.
class ProductNewOut(BaseModel):
    product_id: str
    name: str
    brand: str
    category: str
    price: int
    created_at: str


# 상품을 등록할 때 받는 형식입니다. detail 도 같이 받습니다.
class ProductCreate(BaseModel):
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
    # 이 긴 글이 잘려서 청크가 되고, 그 청크만 새로 임베딩됩니다.
    detail: str


# 청크 한 조각의 정보입니다. 벡터 자체는 숫자 1536개라 보내지 않습니다.
class ChunkInfoOut(BaseModel):
    chunk_id: int
    source: str  # "product" 또는 "review"
    section: str | None
    length: int
    embedded: bool


    
# 상품 하나와, 그 상품이 몇 조각으로 잘렸는지입니다.
class ProductDetailOut(BaseModel):
    product: ProductOut
    detail: str
    chunks: list[ChunkInfoOut]
    # DB 전체 청크 수. 이 상품 청크가 그중 몇 개인지 대비해서 보여주려고 함께 담습니다.
    total_chunks: int   


    
# 등록 결과입니다. 몇 개만 임베딩했는지 보여줍니다.
class ProductCreatedOut(BaseModel):
    product_id: str
    name: str
    # 이번에 새로 만들어 임베딩한 청크 수
    new_chunks: int
    # 전체 청크 수. 이 중 new_chunks 개만 임베딩했다는 뜻입니다.
    total_chunks: int