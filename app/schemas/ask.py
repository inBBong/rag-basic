# AI 질문과 답변의 형식입니다.

from pydantic import BaseModel


# 앞서 주고받은 대화 한 번입니다.
class Turn(BaseModel):
    question: str
    answer: str


class AskRequest(BaseModel):
    question: str

    # 앞서 나눈 대화입니다. 화면이 들고 있다가 질문할 때 같이 보냅니다.
    #
    # AI 는 지난 대화를 기억하지 못합니다. 매번 처음 만나는 사람과 같습니다.
    # 그래서 "이어서 물어보기" 를 하려면 앞 대화를 같이 알려주어야 합니다.
    # 서버가 기억하지 않으므로 서버는 계속 단순한 상태로 남습니다.
    history: list[Turn] = []


# 답을 만들 때 참고한 글 한 조각입니다. RAG 로 답했을 때 채워집니다.
class SourceOut(BaseModel):
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