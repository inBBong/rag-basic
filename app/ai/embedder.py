"""
글을 숫자로 바꿉니다. 이 숫자 묶음을 벡터라고 부릅니다.

뜻이 비슷한 글은 비슷한 숫자가 됩니다. 그래서 숫자끼리 비교하면
"단어는 다르지만 뜻이 비슷한 글" 을 찾아낼 수 있습니다.

예)  "건성 피부에 좋은 토너"  ->  [0.021, -0.043, 0.011, ... ]  (숫자 1536개)
"""

from openai import OpenAI

from app.config import OPENAI_API_KEY

MODEL = "text-embedding-3-small"
DIMENSION = 1536

if not OPENAI_API_KEY:
    raise SystemExit("OPENAI_API_KEY 가 비어 있습니다. .env 파일을 열어 키를 넣어 주세요.")

client = OpenAI(api_key=OPENAI_API_KEY)


def embed_texts(texts):
    """글 여러 개를 한 번에 벡터로 바꿉니다. 하나씩 부르는 것보다 훨씬 빠릅니다."""
    response = client.embeddings.create(model=MODEL, input=texts)
    return [item.embedding for item in response.data]