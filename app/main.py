"""
FastAPI 애플리케이션입니다.

실행: uvicorn app.main:app --reload
문서: http://localhost:8000/docs

요청이 흘러가는 길:
  브라우저 -> api -> services -> repositories -> SQLAlchemy -> DB
"""

from fastapi import FastAPI

from app.api import customers, products

app = FastAPI(title="화장품 AI 관리자")

app.include_router(products.router)
app.include_router(customers.router)


@app.get("/")
def home():
    return {"message": "화장품 AI 관리자 API", "문서": "/docs"}