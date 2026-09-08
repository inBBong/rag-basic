# AI 에게 질문하고 답을 만듭니다.

from app.graph.graph import graph


# 그래프를 시작할 때 넣어줄 첫 값입니다.
def build_state(db, question, history):
    return {
        "db": db,
        "question": question,
        "history": history,
        "route": "",
        "tool_calls": [],
        "tool_result": [],
        "documents": [],
        "answer": "",
        "path": [],
    }


def build_answer(question, result):
    return {
        "question": question,
        "answer": result["answer"],
        "route": result["route"],
        "path": " -> ".join(result["path"]),
        "sources": result["documents"],
        "tool_result": result["tool_result"],
    }


def ask(db, question, history=None):
    result = graph.invoke(build_state(db, question, history or []))
    return build_answer(question, result)


# 진행 상황을 두 가지로 내보냅니다.
def ask_stream(db, question, history=None):
    result = {}

    state = build_state(db, question, history or [])

    for source, data in graph.stream(state, stream_mode=["updates", "custom"]):
        if source == "custom":
            yield {"type": "piece", "text": data["piece"]}
            continue

        for name, filled in data.items():
            result.update(filled)
            # route 를 같이 보내면 화면에서 칸 색을 바로 칠할 수 있습니다.
            yield {"type": "node", "name": name, "route": result.get("route", "")}

    yield {"type": "done", **build_answer(question, result)}