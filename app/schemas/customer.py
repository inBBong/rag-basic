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