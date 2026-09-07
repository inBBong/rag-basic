"""
바깥 AI 로 보내기 전에 개인정보를 가립니다.

  DB 조회 결과 / 검색 결과  ->  mask()  ->  OpenAI

가려야 할 연락처가 두 군데에 있습니다.

  컬럼    고객 테이블의 phone / email
  글 속   고객이 후기 본문에 직접 적어 넣은 것

컬럼은 SQL 에서 빼면 되지만, 글 속에 섞인 것은 뺄 수가 없습니다.
그래서 본문을 읽어서 찾아 가립니다.

가린 값은 되돌리지 않습니다. 그래서 AI 는 진짜 번호를 끝까지 알 수 없습니다.

직접 확인해 보기:
    python -m app.ai.masking
"""

import re

EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+")
PHONE = re.compile(r"0\d{1,2}-?\d{3,4}-?\d{4}")


def hide_email(match):
    """eunsu45@example.com  ->  eu***@example.com"""
    name, _, domain = match.group().partition("@")
    return f"{name[:2]}***@{domain}"


def mask(text):
    if not text:
        return text

    text = EMAIL.sub(hide_email, text)
    text = PHONE.sub("0**-****-****", text)
    return text


def mask_chunks(chunks):
    """검색해 온 청크들의 본문을 가립니다."""
    return [dict(chunk, content=mask(chunk["content"])) for chunk in chunks]


def mask_rows(rows):
    """도구가 DB 에서 가져온 결과를 가립니다.

    고객 조회 결과에는 전화번호와 이메일이 그대로 들어있습니다.
    글자로 된 값만 가리고 숫자는 그대로 둡니다.
    """
    return [
        {key: mask(value) if isinstance(value, str) else value for key, value in row.items()}
        for row in rows
    ]


def show_customers():
    """컬럼에 들어있는 연락처입니다."""
    from app.db import SessionLocal
    from app.models.customer import Customer

    db = SessionLocal()
    for customer in db.query(Customer).limit(3).all():
        line = f"{customer.name} / {customer.phone} / {customer.email}"
        print(f"  전 : {line}")
        print(f"  후 : {mask(line)}")
        print()
    db.close()


def show_reviews():
    """후기 본문에 고객이 직접 적어 넣은 연락처입니다.

    DB 가 아니라 원본 CSV 를 읽습니다. 청크는 저장하기 전에 이미 가려서
    넣기 때문에, DB 에서는 가리기 전 모습을 볼 수 없습니다.
    """
    import csv

    with open("data/reviews.csv", encoding="utf-8") as f:
        rows = [row["content"] for row in csv.DictReader(f)]

    found = [text for text in rows if EMAIL.search(text) or PHONE.search(text)]
    print(f"  후기 {len(rows)}건 중 {len(found)}건에 연락처가 들어있습니다.")
    print()

    for text in found[:2]:
        print(f"  전 : {text}")
        print(f"  후 : {mask(text)}")
        print()


def main():
    print("=== 컬럼에 들어있는 연락처 (고객 테이블) ===")
    show_customers()
    print("=== 글 속에 섞여 있는 연락처 (후기 본문) ===")
    show_reviews()


if __name__ == "__main__":
    main()