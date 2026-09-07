# 화장품 AI 관리자 — 실습 시작 폴더

여기에는 **데이터와 설정만** 들어 있습니다.
코드는 수업에서 단계별로 직접 채워 넣습니다.

---

## 1. 준비물

| | |
|---|---|
| 파이썬 | **3.10 이상** (3.11 이상 권장) |
| OpenAI 키 | https://platform.openai.com/api-keys 에서 발급 |
| 편집기 | VS Code 등 아무거나 |

파이썬이 깔려 있는지 확인해 보세요.

```
python --version
```

`Python 3.13.7` 처럼 나오면 됩니다.
`python` 이 없다는 말이 나오면 https://www.python.org 에서 설치하세요.
설치할 때 **Add Python to PATH** 를 꼭 체크합니다.

---

## 2. 내려받기

깃허브 페이지에서 **Code → Download ZIP** 을 누릅니다.
받은 파일의 압축을 풀고, 그 폴더를 편집기로 엽니다.

폴더 이름에 **한글이나 띄어쓰기가 없는 편**이 좋습니다.

---

## 3. 설치 — 터미널에 네 줄

편집기에서 터미널을 엽니다. (VS Code 는 `Ctrl` + `` ` ``)

### 윈도우

```
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 맥 · 리눅스

```
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

줄 앞에 `(.venv)` 가 붙으면 성공입니다.

```
(.venv) C:\...\rag-basic>
```

> **가상환경이 뭔가요**
> 이 프로젝트에서만 쓸 패키지를 담아두는 상자입니다.
> 컴퓨터 전체가 아니라 `.venv` 폴더 안에만 깔려서, 다른 작업과 섞이지 않습니다.
> **터미널을 새로 열 때마다 `activate` 를 다시 해야 합니다.**

---

## 4. 키 넣기

폴더 안의 `.env` 파일을 열고 첫 칸을 채웁니다.

```
OPENAI_API_KEY=sk-여기에-붙여넣기
```

따옴표는 넣지 않습니다. `=` 뒤에 바로 붙입니다.

`.env` 는 **절대 다른 사람에게 주지 마세요.**

> 키는 4단계까지는 없어도 됩니다. 5단계(임베딩)부터 필요합니다.

---

## 5. 폴더가 왜 비어 있나요

```
rag-basic/
├─ data/          CSV 4개. 여기서 모든 게 시작합니다.
├─ pipeline/      데이터를 DB 와 벡터로 바꾸는 준비 스크립트
├─ app/           서버 코드
│  ├─ models/         테이블 정의
│  ├─ schemas/        주고받는 형식
│  ├─ repositories/   DB 조회
│  ├─ services/       업무 로직
│  ├─ api/            엔드포인트
│  ├─ ai/             AI 호출
│  ├─ rag/            검색·리랭킹
│  ├─ tools/          AI 도구
│  └─ graph/          흐름 제어
├─ tests/         테스트
├─ eval/          답변 품질 채점
├─ web/           화면
├─ .env           API 키
└─ requirements.txt
```

폴더는 미리 만들어 뒀고, **파일은 수업에서 하나씩 만듭니다.**
각 폴더의 `__init__.py` 는 "이 폴더는 파이썬 패키지" 라는 표시일 뿐, 내용은 비어 있습니다.

---

## 6. 앞으로 하게 될 일

단계마다 **터미널에서 눈으로 확인할 결과**가 하나씩 늘어납니다.

| 단계 | 만드는 것 | 확인 |
|---|---|---|
| 1 | 후기 분리 | `python -m pipeline.split_reviews` |
| 2 | DB 적재 | `python -m pipeline.load_data` |
| 3 | FastAPI 3계층 | `uvicorn app.main:app --reload` → `/docs` |
| 4 | 청킹 + 마스킹 | `python -m pipeline.chunk` → 3,060개 |
| 5 | 임베딩 | `python -m pipeline.embed` → 1,536차원 |
| 6 | 벡터 검색 | `python -m app.rag.retriever "질문"` |
| 7 | 기본 RAG | `POST /ask` |
| 8~12 | 리랭커 · 도구 · 그래프 · 증분 임베딩 · 스트리밍 | |
| 13~16 | 화면 4개 | `http://localhost:8000` |
| 17~22 | 테스트 · 추천 · 평가 · 추적 | `pytest` |

1~5단계를 한 번에 돌리는 명령도 나중에 만듭니다.

```
python -m pipeline.run_all
```

---

## 7. 자주 나는 문제

**`python` 을 찾을 수 없습니다**
파이썬을 설치할 때 **Add Python to PATH** 를 체크하지 않은 경우입니다.
다시 설치하면서 체크하거나, `py -m venv .venv` 로 해보세요.

**`(.venv)` 가 안 보입니다**
`activate` 를 안 했거나, 터미널을 새로 연 것입니다.
윈도우에서 실행 정책 오류가 나면 이렇게 한 번 실행하고 다시 해보세요.

```
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

**`ModuleNotFoundError: No module named 'app'`**
프로젝트 **최상위 폴더**(이 README 가 있는 곳)에서 실행해야 합니다.
그리고 `python pipeline/load_data.py` 가 아니라
`python -m pipeline.load_data` 처럼 **`-m`** 을 붙입니다.

**`OPENAI_API_KEY 가 비어 있습니다`**
`.env` 파일의 첫 칸이 비어 있습니다. 키를 넣고 다시 실행하세요.

**포트가 이미 쓰이고 있습니다**
`uvicorn app.main:app --reload --port 8001` 처럼 번호를 바꿔 보세요.

---

## 8. 처음부터 다시 하고 싶을 때

만들어진 DB 파일을 지우고 준비 작업을 다시 돌리면 됩니다.

```
del cosmetic.db          윈도우
rm cosmetic.db           맥·리눅스
```

`data/` 안의 CSV 를 되돌리려면 ZIP 을 다시 받는 것이 가장 확실합니다.
1단계는 `purchases.csv` 를 고쳐 쓰기 때문입니다.
