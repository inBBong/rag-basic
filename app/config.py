import os

from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./cosmetic.db")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# 답변 생성·리랭킹에 쓸 모델입니다. .env 에서 바꿀 수 있습니다.
# 임베딩 모델은 여기 없습니다. 바꾸면 이미 저장한 벡터가 쓸모없어져서
# app/ai/embedder.py 에 고정해 두었습니다.
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")