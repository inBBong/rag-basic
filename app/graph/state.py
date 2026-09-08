# 그래프가 들고 다니는 값입니다.

from typing import TypedDict

from sqlalchemy.orm import Session


class GraphState(TypedDict):
    # DB 세션. 노드가 DB 를 쓰려면 필요해서 같이 들고 다닙니다.
    db: Session

    question: str

    # plan 이 정합니다. "tool" 또는 "rag"
    route: str

    # plan 이 고른 도구들. [{"name": "get_top_customers", "arguments": {"limit": 5}}]
    tool_calls: list

    # run_tools 가 DB 에서 가져온 결과
    tool_result: list

    # retrieve 와 rerank 가 찾아온 글 조각
    documents: list

    # generate 가 만든 최종 답변
    answer: str

    # 어떤 노드를 거쳐 왔는지. 화면에 보여주려고 기록합니다.
    path: list