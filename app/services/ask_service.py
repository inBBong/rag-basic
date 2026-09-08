
"""
def ask(db, question):
    candidates = retrieve(db, question, CANDIDATES)
    chunks = rerank(question, candidates, TOP_K)
    chunks = masking.mask_chunks(chunks)

    user_prompt = prompts.build_rag_prompt(question, chunks)
    answer = llm.ask(prompts.RAG_SYSTEM, user_prompt)

    return {"question": question, "answer": answer, "sources": chunks}
"""

# AI 에게 질문하고 답을 만듭니다.

from app.graph.graph import graph


# 그래프를 시작할 때 넣어줄 첫 값입니다.
def build_state(db, question):
    return {
        "db": db,
        "question": question,
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


def ask(db, question):
    result = graph.invoke(build_state(db, question))
    return build_answer(question, result)