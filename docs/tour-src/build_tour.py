"""
코드 투어 교안(docs/tour.html)을 다시 만듭니다.

실행:
    python docs/tour-src/build_tour.py

본문(t0~t7.html)에 {{CODE:app/db.py}} 라고 적어두면
course 브랜치의 실제 파일 내용으로 바꿔 넣습니다.
손으로 옮겨 적지 않으므로 코드가 교안과 어긋날 일이 없습니다.

    {{CODE:경로}}    그 파일의 전체 내용
    {{LINES:경로}}   그 파일이 몇 줄인지

코드를 고친 뒤 이 스크립트를 다시 돌리면 교안이 최신 코드로 갱신됩니다.
"""

import html
import pathlib
import re
import subprocess
import sys

HERE = pathlib.Path(__file__).parent
REPO = HERE.parent.parent
BRANCH = "course"

PARTS = ["tour-head.part"] + [f"t{n}.html" for n in range(8)] + ["tour-tail.part"]
OUTPUT = REPO / "docs" / "tour.html"

_cache = {}


def source(path):
    """course 브랜치에서 파일 내용을 읽어옵니다."""
    if path not in _cache:
        result = subprocess.run(
            ["git", "show", f"{BRANCH}:{path}"],
            cwd=REPO, capture_output=True, text=True, encoding="utf-8",
        )
        if result.returncode != 0:
            raise SystemExit(f"{BRANCH} 브랜치에 없는 파일입니다: {path}")
        _cache[path] = result.stdout.rstrip("\n")
    return _cache[path]


def expand(text):
    text = re.sub(r"\{\{CODE:([^}]+)\}\}", lambda m: html.escape(source(m.group(1)), quote=False), text)
    text = re.sub(r"\{\{LINES:([^}]+)\}\}", lambda m: str(len(source(m.group(1)).splitlines())), text)
    return text


def main():
    pieces = []
    for name in PARTS:
        body = (HERE / name).read_text(encoding="utf-8")
        pieces.append(body if name.endswith(".part") else expand(body).rstrip() + "\n\n")

    OUTPUT.write_text("".join(pieces), encoding="utf-8")

    text = OUTPUT.read_text(encoding="utf-8")
    print(f"{OUTPUT.relative_to(REPO)} 생성")
    print("  슬라이드", text.count('class="slide"'))
    print("  실은 파일", len(_cache), "개")

    for tag in ["section", "div", "pre", "details"]:
        opened, closed = text.count("<" + tag), text.count("</" + tag + ">")
        mark = "" if opened == closed else "   <- 짝이 안 맞습니다"
        print(f"  <{tag}> {opened} / </{tag}> {closed}{mark}")


if __name__ == "__main__":
    sys.exit(main())
