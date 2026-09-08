# 노드들을 이어 붙여 그래프를 만듭니다.

from langgraph.graph import END, START, StateGraph

from app.graph import nodes
from app.graph.state import GraphState


# plan 이 정해 둔 값을 그대로 읽습니다. "tool" 또는 "rag" 입니다.
def choose_route(state):
    return state["route"]


def build_graph():
    builder = StateGraph(GraphState)

    builder.add_node("plan", nodes.plan)
    builder.add_node("run_tools", nodes.run_tools)
    builder.add_node("retrieve", nodes.retrieve)
    builder.add_node("rerank", nodes.rerank)
    builder.add_node("mask", nodes.mask)
    builder.add_node("generate", nodes.generate)

    builder.add_edge(START, "plan")
    builder.add_conditional_edges("plan", choose_route, {"tool": "run_tools", "rag": "retrieve"})
    builder.add_edge("run_tools", "mask")
    builder.add_edge("retrieve", "rerank")
    builder.add_edge("rerank", "mask")
    builder.add_edge("mask", "generate")
    builder.add_edge("generate", END)

    return builder.compile()


# 그래프는 한 번만 만들어 두고 계속 씁니다.
graph = build_graph()