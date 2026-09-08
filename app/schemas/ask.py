"""AI 질문과 답변의 형식입니다."""

from pydantic import BaseModel


class AskRequest(BaseModel):
    question: str


class SourceOut(BaseModel):
    """답을 만들 때 참고한 글 한 조각입니다."""

    source: str  # "product" 또는 "review"
    source_id: str
    product_id: str
    section: str | None
    score: float
    content: str


class AskResponse(BaseModel):
    question: str
    answer: str
    # "tool" 또는 "rag". 어느 길로 답했는지입니다.
    route: str
    # 어떤 노드를 거쳐 왔는지. 예) "plan -> retrieve -> rerank -> mask -> generate"
    path: str
    # AI 가 무엇을 보고 답했는지 같이 돌려줍니다.
    # 답이 이상할 때 검색이 문제인지 AI 가 문제인지 바로 구분할 수 있습니다.
    sources: list[SourceOut]
    # 도구로 답했을 때 DB 에서 가져온 결과입니다. 개인정보는 가려져 있습니다.
    tool_result: list[dict]