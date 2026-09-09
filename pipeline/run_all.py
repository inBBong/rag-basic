"""
데이터 준비를 처음부터 끝까지 한 번에 합니다.

실행: python -m pipeline.run_all

    후기 분리  ->  DB 적재  ->  청킹  ->  임베딩

각 단계를 따로 돌리고 싶으면 아래처럼 하나씩 실행해도 됩니다.
    python -m pipeline.split_reviews
    python -m pipeline.load_data
    python -m pipeline.chunk
    python -m pipeline.embed
"""

from pipeline import chunk, embed, load_data, split_review


def run(step_name, step):
    print()
    print("=" * 60)
    print(step_name)
    print("=" * 60)
    step.main()


def main():
    run("1. 후기 분리", split_review)
    run("2. DB 적재", load_data)
    run("3. 청킹", chunk)
    run("4. 임베딩", embed)

    print()
    print("=" * 60)
    print("준비 완료. 이제 서버를 켜세요.")
    print("  uvicorn app.main:app --reload")
    print("=" * 60)


if __name__ == "__main__":
    main()