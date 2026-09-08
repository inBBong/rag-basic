"""
OpenAI 에게 질문하고 답을 받아옵니다.

모델은 .env 의 OPENAI_MODEL 로 정합니다. 코드를 고치지 않고 바꿀 수 있습니다.
쓸 수 있는 이름은 계정마다 다릅니다. 없는 이름을 넣으면 404 가 나고
과금도 되지 않으므로, 안 되면 다른 이름으로 바꿔 보면 됩니다.
"""

from openai import OpenAI

from app.config import OPENAI_API_KEY, OPENAI_MODEL

if not OPENAI_API_KEY:
    raise SystemExit("OPENAI_API_KEY 가 비어 있습니다. .env 파일을 열어 키를 넣어 주세요.")

client = OpenAI(api_key=OPENAI_API_KEY)

# llm으로부터 문자 답변을 받기 위한 요청함수
def ask(system_prompt, user_prompt):
    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )
    return response.choices[0].message.content


# 도구 목록을 같이 건네고, AI 가 도구를 고르는지 봅니다. (문자값을 받는게 아니라 객체를 전달받기 위함)
def ask_with_tools(system_prompt, user_prompt, tool_specs):
    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        tools=tool_specs,
    )
    return response.choices[0].message