# AI 에게 질문하는 엔드포인트입니다.

import json

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.db import SessionLocal, get_db
from app.schemas.ask import AskRequest, AskResponse
from app.services import ask_service

router = APIRouter()


@router.post("/ask", response_model=AskResponse)
def ask(request: AskRequest, db: Session = Depends(get_db)):
    history = [turn.model_dump() for turn in request.history]
    return ask_service.ask(db, request.question, history)


# 단계가 끝날 때마다 한 줄씩 내려보냅니다.
@router.post("/ask/stream")
def ask_stream(request: AskRequest):
    history = [turn.model_dump() for turn in request.history]

    def events():
        db = SessionLocal()
        try:
            for event in ask_service.ask_stream(db, request.question, history):
                yield "data: " + json.dumps(event, ensure_ascii=False) + "\n\n"
        finally:
            db.close()

    return StreamingResponse(events(), media_type="text/event-stream")