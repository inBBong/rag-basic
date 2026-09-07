"""
데이터베이스 연결을 담당합니다. 이 파일이 가진 것은 네 가지뿐입니다.

engine        실제 DB 와 연결하는 통로
SessionLocal  DB 작업 한 번에 쓰는 세션을 만들어 주는 공장
Base          모든 테이블 모델이 물려받는 기준
get_db        요청 하나마다 세션을 열고 닫아 주는 함수
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.config import DATABASE_URL

# SQLite 는 여러 스레드에서 접근할 때 이 옵션이 필요합니다. PostgreSQL 은 필요 없습니다.
# 이렇게 해두면 Supabase 로 옮길 때 이 파일은 고치지 않아도 됩니다.
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
# 특정 사용자 전용의 DB제어 작업 공간 생성 (이때 필요한게 sqlalchemy의 engine객체)
SessionLocal = sessionmaker(bind=engine)
# 테이블 스키마 등록된 클래스를 만들고 해당 Base객체를 상속만 먹이면 자동으로 sql없이 테이블 생성됨
Base = declarative_base()


# 브라우저에서 라우터 요청이 들어왔을떄 실제 DB제어 작업이 끝나기 전까지 DB 세션을 종료하지 않게하기 위한 헬퍼 함수
def get_db():
    db = SessionLocal()
    try:
        # FAST API한테 작업 완료 권한을 넘겨줌
        yield db
    finally:
        db.close()