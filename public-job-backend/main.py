from fastapi import FastAPI
from app.database import Base, engine
from app.routers import postings
from app.routers import users  # 사용자 라우터 임포트

# DB 테이블 생성
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Public Jobs API", version="1.0")

# 라우터 등록
app.include_router(postings.router)
# 사용자 라우터 등록
app.include_router(users.router)

@app.get("/")
def read_root():
    return {"message": "공기업 채용 알림 서버 정상 작동 중 🚀"}
