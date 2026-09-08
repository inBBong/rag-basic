# 상품을 JSON 으로 내보낼 때의 형식입니다.

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


# 등록 결과입니다. 몇 개만 임베딩했는지 보여줍니다.
class ProductCreatedOut(BaseModel):
    product_id: str
    name: str

    # 이번에 새로 만들어 임베딩한 청크 수
    new_chunks: int

    # 전체 청크 수. 이 중 new_chunks 개만 임베딩했다는 뜻입니다.
    total_chunks: int