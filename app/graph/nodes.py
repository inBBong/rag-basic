# 그래프의 노드 6개입니다.

import json

from langgraph.config import get_stream_writer

from app.ai import llm, masking, prompts
from app.rag.reranker import rerank as rerank_chunks
from app.rag.retriever import retrieve as retrieve_chunks
from app.tools import tools

CANDIDATES = 20
TOP_K = 4


# 도구를 쓸지 검색을 할지 정합니다.
def plan(state):
    user_prompt = prompts.build_history(state["history"]) + state["question"]
    message = llm.ask_with_tools(prompts.PLAN_SYSTEM, user_prompt, tools.TOOL_SPECS)

    if not message.tool_calls:
        return {"route": "rag", "path": state["path"] + ["plan"]}

    tool_calls = [
        {"name": call.function.name, "arguments": json.loads(call.function.arguments)}
        for call in message.tool_calls
    ]
    return {"route": "tool", "tool_calls": tool_calls, "path": state["path"] + ["plan"]}


# plan 이 고른 도구를 실제로 실행합니다.
def run_tools(state):
    rows = []
    for call in state["tool_calls"]:
        rows += tools.run_tool(state["db"], call["name"], call["arguments"])

    return {"tool_result": rows, "path": state["path"] + ["run_tools"]}


# 질문과 비슷한 글을 찾아옵니다.
def retrieve(state):
    search_text = prompts.build_history(state["history"]) + state["question"]

    documents = retrieve_chunks(state["db"], search_text, CANDIDATES)
    return {"documents": documents, "path": state["path"] + ["retrieve"]}


def rerank(state):
    documents = rerank_chunks(state["question"], state["documents"], TOP_K)
    return {"documents": documents, "path": state["path"] + ["rerank"]}


# AI 로 보내기 직전에 개인정보를 가립니다.
def mask(state):
    return {
        "tool_result": masking.mask_rows(state["tool_result"]),
        "documents": masking.mask_chunks(state["documents"]),
        "path": state["path"] + ["mask"],
    }


# 답을 만듭니다. 온 길에 따라 참고 자료가 다릅니다.
def generate(state):
    if state["route"] == "tool":
        system_prompt = prompts.TOOL_SYSTEM
        user_prompt = prompts.build_tool_prompt(
            state["question"], state["tool_result"], state["history"]
        )
    else:
        system_prompt = prompts.RAG_SYSTEM
        user_prompt = prompts.build_rag_prompt(
            state["question"], state["documents"], state["history"]
        )

    write = get_stream_writer()
    pieces = []

    for piece in llm.ask_stream(system_prompt, user_prompt):
        pieces.append(piece)
        write({"piece": piece})

    return {"answer": "".join(pieces), "path": state["path"] + ["generate"]}