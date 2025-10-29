import os
from dotenv import load_dotenv

# SQLAlchemy 임포트
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Firebase Admin SDK 임포트
import firebase_admin
from firebase_admin import credentials, firestore

# .env 파일 로드
load_dotenv()

# ==========================================================
# 1. 환경 변수 로드
# ==========================================================
# MySQL 환경 변수
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# Firebase 환경 변수 (새로 추가)
FIREBASE_KEY_PATH = os.getenv("FIREBASE_KEY_PATH")

# ==========================================================
# 2. SQLAlchemy 설정 (MySQL)
# ==========================================================
# MySQL 연결 URL
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# SQLAlchemy 엔진, 세션 및 베이스
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 의존성 주입용 세션 함수
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ==========================================================
# 3. Firebase Admin SDK 초기화
# ==========================================================
# 초기화된 Firestore 클라이언트를 저장할 전역 변수
db_firebase = None

def initialize_firebase():
    """Firebase Admin SDK를 초기화하고 Firestore 클라이언트를 반환합니다."""
    global db_firebase
    
    # 이미 초기화되었는지 확인 (FastAPI의 hot-reload 및 중복 초기화 방지)
    if firebase_admin._apps:
        return firestore.client()
    
    if not FIREBASE_KEY_PATH:
        print("❌ [FIREBASE] 환경 변수 FIREBASE_KEY_PATH가 설정되지 않아 Firebase 초기화를 건너뜁니다.")
        return None
        
    try:
        # 서비스 계정 키 경로로 인증 정보 생성
        cred = credentials.Certificate(FIREBASE_KEY_PATH)
        
        # Firebase 앱 초기화
        firebase_admin.initialize_app(cred)
        print("✅ [FIREBASE] Admin SDK가 성공적으로 초기화되었습니다.")
        
        # Firestore 클라이언트 반환
        return firestore.client()

    except Exception as e:
        print(f"❌ [FIREBASE] 초기화 실패: {e}")
        return None

# 파일이 로드될 때 Firebase를 초기화하고 클라이언트를 전역 변수에 저장
db_firebase = initialize_firebase()