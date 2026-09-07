"""
AI 에게 질문하는 엔드포인트입니다.

  POST /ask
  { "question": "비타민C 필링 로션은 어떤 피부에 맞아?" }
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import get_db
from app.schemas.ask import AskRequest, AskResponse
from app.services import ask_service

router = APIRouter()


@router.post("/ask", response_model=AskResponse)
def ask(request: AskRequest, db: Session = Depends(get_db)):
    return ask_service.ask(db, request.question)