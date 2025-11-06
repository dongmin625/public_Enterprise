from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware # 1. CORS 임포트
from app.database import Base, engine
from app.routers import postings
from app.routers import users # 사용자 라우터 임포트

# DB 테이블 생성
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Public Jobs API", version="1.0")

# ↓↓↓↓ 2. CORS 미들웨어 등록 (가장 먼저 위치해야 함) ↓↓↓↓

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://192.168.35.109:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,              # 허용할 출처 목록
    allow_credentials=True,             # 쿠키 허용
    allow_methods=["*"],                # 모든 HTTP 메서드 허용 (OPTIONS, GET, POST 등)
    allow_headers=["*"],                # 모든 헤더 허용 (Authorization 헤더 포함)
)
# ↑↑↑↑ CORS 미들웨어는 여기에 있어야 합니다 ↑↑↑↑

# 3. 라우터 등록 (CORS 미들웨어 등록 후)
app.include_router(postings.router)
# 사용자 라우터 등록
app.include_router(users.router)

@app.get("/")
def read_root():
    return {"message": "공기업 채용 알림 서버 정상 작동 중 🚀"}