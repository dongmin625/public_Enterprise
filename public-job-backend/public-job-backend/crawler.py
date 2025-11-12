# crawler.py

import requests
import os
from bs4 import BeautifulSoup
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, DATABASE_URL  # DB 연결 URL과 Base를 재사용
from app.models import JobPosting        # 공고 모델 임포트

# ------------------------------------------------------------------
# DB 연결 설정 (FastAPI와 동일한 설정 사용)
# ------------------------------------------------------------------
# 주의: DATABASE_URL은 app/database.py가 로드될 때 설정되어야 합니다.
# (Python이 app.database를 읽을 때 DATABASE_URL이 정의되도록 프로젝트 구조가 되어 있다고 가정합니다.)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """크롤러용 DB 세션 생성 함수"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def run_crawler():
    db_generator = get_db()
    db = next(db_generator) # DB 세션 인스턴스를 가져옴
    
    # 🚨 [중요] 여기에 실제 크롤링할 웹사이트 URL을 입력하세요.
    URL = "http://example.com" 
    
    try:
        # --- 예시 데이터 추출 (실제 크롤링 로직으로 대체해야 함) ---
        extracted_data = [
            {
                'company_name': 'AWS EC2 테스트 기업',
                'job_type': '정규직',
                'title': f'EC2 환경 크롤링 테스트 공고 {i}',
                'link': URL + f"/detail/{i}",
                'start_date': '2025-11-12', 
                'end_date': '2025-12-31',
            } for i in range(1, 4) # 3개의 테스트 데이터 생성
        ]
        # --------------------------------------------------------
        
        # 3. 데이터베이스에 저장
        new_postings = []
        for data in extracted_data:
            # 중복 검사 로직을 추가해야 하지만, 여기서는 간단히 저장합니다.
            new_postings.append(JobPosting(**data))

        db.add_all(new_postings)
        db.commit()
        
        print(f"✅ SUCCESS: {len(new_postings)}개의 공고 정보를 DB에 저장했습니다.")

    except requests.exceptions.RequestException as e:
        print(f"❌ ERROR: HTTP 요청 오류 발생: {e}")
    except Exception as e:
        print(f"❌ ERROR: 데이터 처리 중 오류 발생: {e}")
    finally:
        db_generator.close()

if __name__ == "__main__":
    # DB 테이블이 없으면 생성
    Base.metadata.create_all(bind=engine)
    
    # 크롤러 실행
    run_crawler()