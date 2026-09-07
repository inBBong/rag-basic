import csv
from pathlib import Path

DATA = Path(__file__).parent.parent / "data"

# 기존 PURCHASE CSV에서 구매정보와 후기를 각각 분리해서 나눠 담을 새로운 CSV 파일 생성 경로
PURCHASES = DATA / "purchases.csv"
REVIEWS = DATA / "reviews.csv"

# 앞으로 만들 PURCHASE, REVIEW 테이블에 넣을 컬럼 이름 미리 리스트에 등록
PURCHASE_COLUMNS = ["purchase_id", "customer_id", "product_id", "purchased_at", "quantity"]
REVIEW_COLUMNS = ["review_id", "purchase_id", "customer_id", "product_id", "rating", "content", "written_at"]


# CSV파일 경로를 인자로 전달받아 리스트 형태로 반환하는 함수
def read_csv(path):
    with open(path, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


# 새로운 csv 파일 생성
def write_csv(path, rows, columns):
    # lineterminator 를 "\n" 으로 두면 윈도우와 맥에서 파일이 똑같이 만들어집니다
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=columns, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

# purchase.csv에 들어갈 값을 선별해서 생성 함수
def make_purchase(row):
    return {
        "purchase_id": row["purchase_id"],
        "customer_id": row["customer_id"],
        "product_id": row["product_id"],
        "purchased_at": row["purchased_at"],
        "quantity": row["quantity"],
    }


# review.csv에 들어갈 값을 선별해서 생성 함수
def make_review(row, number):
    return {
        "review_id": f"R{number:04d}",
        "purchase_id": row["purchase_id"],
        "customer_id": row["customer_id"],
        "product_id": row["product_id"],
        "rating": row["rating"],
        "content": row["review"],
        "written_at": row["purchased_at"],
    }


def main():
    rows = read_csv(PURCHASES)

    if "review" not in rows[0]:
        print("이미 분리되어 있습니다. 아무것도 하지 않습니다.")
        return

    purchases = [make_purchase(row) for row in rows]
    reviews = [make_review(row, number) for number, row in enumerate(rows, start=1)]

    write_csv(PURCHASES, purchases, PURCHASE_COLUMNS)
    write_csv(REVIEWS, reviews, REVIEW_COLUMNS)


if __name__ == "__main__":
    main()

