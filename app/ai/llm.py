# OpenAI 에게 질문하고 답을 받아옵니다.

from openai import OpenAI

from app.config import OPENAI_API_KEY, OPENAI_MODEL

if not OPENAI_API_KEY:
    raise SystemExit("OPENAI_API_KEY 가 비어 있습니다. .env 파일을 열어 키를 넣어 주세요.")

client = OpenAI(api_key=OPENAI_API_KEY)


def ask(system_prompt, user_prompt):
    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )
    return response.choices[0].message.content


# 답을 조각조각 받아옵니다.
def ask_stream(system_prompt, user_prompt):
    pieces = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        stream=True,
    )

    for piece in pieces:
        if piece.choices and piece.choices[0].delta.content:
            yield piece.choices[0].delta.content


# 도구 목록을 같이 건네고, AI 가 도구를 고르는지 봅니다.
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