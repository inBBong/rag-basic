# AI 가 고를 수 있는 도구 목록입니다.

import json
import sys

from app.ai import llm, prompts
from app.services import customer_service, product_service


# 이름과 실제 함수를 이어줍니다. AI 는 이름만 알려주기 때문입니다.
TOOLS = {
    "get_top_customers": customer_service.get_top_spenders,
    "get_best_selling_products": product_service.get_best_selling,
    "count_customers_by_skin_type": customer_service.count_by_skin_type,
    "get_products_by_category": product_service.get_product_summaries,
}


# AI 에게 보여줄 도구 설명서입니다.
# description 을 보고 AI 가 어떤 도구를 쓸지 정하므로, 설명을 정확하게 씁니다.
TOOL_SPECS = [
    {
        "type": "function",
        "function": {
            "name": "get_top_customers",
            "description": "구매 금액이 가장 큰 고객을 순서대로 찾습니다. 우수 고객, 큰손, 구매액 순위 질문에 씁니다.",
            "parameters": {
                "type": "object",
                "properties": {"limit": {"type": "integer", "description": "몇 명까지 볼지. 기본 5"}},
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_best_selling_products",
            "description": "판매 수량이 가장 많은 상품을 순서대로 찾습니다. 인기 상품, 잘 팔리는 상품 질문에 씁니다.",
            "parameters": {
                "type": "object",
                "properties": {"limit": {"type": "integer", "description": "몇 개까지 볼지. 기본 5"}},
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "count_customers_by_skin_type",
            "description": "피부 타입별로 고객이 몇 명인지 셉니다. 건성, 지성, 복합성, 중성, 민감성 분포를 볼 때 씁니다.",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_products_by_category",
            "description": "카테고리에 속한 상품 목록을 찾습니다. 카테고리는 토너, 로션, 크림, 세럼, 앰플, 미스트, 선크림, 에센스, 클렌징폼, 클렌징오일 입니다.",
            "parameters": {
                "type": "object",
                "properties": {
                    "category": {"type": "string", "description": "상품 카테고리"},
                    "limit": {"type": "integer", "description": "몇 개까지 볼지. 기본 10"},
                },
                "required": ["category"],
            },
        },
    },
]


# AI 가 고른 도구를 실제로 실행합니다.
def run_tool(db, name, arguments):
    # arguments 는 {"limit": 5} 같은 딕셔너리입니다.
    # ** 를 붙이면 limit=5 처럼 인자로 풀어서 넘겨줍니다.
    # TOOLS["get_products_by_category"] -> get_product_summaries 함수 정의형태
    # 위에서 불러온 정의형태의 함수에 ()를 붙여서 호출
    return TOOLS[name](db, **arguments) 


def main():
    from app.db import SessionLocal

    question = sys.argv[1] if len(sys.argv) > 1 else "구매액이 가장 높은 고객 5명"
    message = llm.ask_with_tools(prompts.PLAN_SYSTEM, question, TOOL_SPECS)

    print(f"질문: {question}")
    print()

    if not message.tool_calls:
        print("  AI 가 도구를 고르지 않았습니다.")
        print("  -> 글을 읽어야 답할 수 있는 질문이므로 RAG 로 처리합니다.")
        return

    db = SessionLocal()
    for call in message.tool_calls:
        arguments = json.loads(call.function.arguments)
        print(f"  AI 가 고른 도구: {call.function.name}({arguments})")
        result = run_tool(db, call.function.name, arguments)
        print(f"  DB 결과 {len(result)}건")
        for row in result:
            print(f"    {row}")
    db.close()


if __name__ == "__main__":
    main()