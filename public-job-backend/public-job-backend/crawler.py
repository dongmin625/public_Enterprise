# crawler.py

import requests
from bs4 import BeautifulSoup
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import date, datetime
import re # 정규표현식 라이브러리 임포트

# FastAPI 프로젝트에서 DB 설정과 모델을 재사용
from app.database import Base, DATABASE_URL
from app.models import JobPosting        
from app.database import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT # DB 접속 정보 재사용

# ------------------------------------------------------------------
# 1. 크롤링 대상 URL 목록 정의 (EWP 단일 대상)
# ------------------------------------------------------------------
EWP_URL = "https://www.ewp.co.kr/kor/subpage/content.html?pc=SP5RQGKR3BAUE4W1XB8Q9IE8WF9WA4U"
JOB_SITES = [
    {"name": "한국동서발전", "url": EWP_URL, "parser": "parse_ewp"},
]

# ------------------------------------------------------------------
# 2. DB 연결 및 세션 생성 설정
# ------------------------------------------------------------------
# 주의: app.database에서 DB URL이 설정되어 있어야 합니다.
# 만약 app.database가 제대로 로드되지 않는다면 아래처럼 직접 URL을 구성할 수 있습니다.
# DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """크롤러용 DB 세션 생성 함수"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ------------------------------------------------------------------
# 3. 파싱 함수 정의 (한국동서발전 HTML 구조 기반)
# ------------------------------------------------------------------
def parse_ewp(soup, site_name, base_url):
    data = []
    
    # 1. 테이블 찾기: 'tableL' 클래스를 가진 테이블 사용
    table = soup.find('table', class_='tableL') 
    if not table:
        print("경고: 채용 공고 테이블(tableL)을 찾을 수 없습니다. 셀렉터를 확인하세요.")
        return data

    # 2. 모든 데이터 행(tr) 순회
    rows = table.find('tbody').find_all('tr') if table.find('tbody') else table.find_all('tr')

    # 공고 상세 페이지 URL의 기본 주소 (상대 경로를 위한 기본 URL)
    base_view_url = base_url.split('?')[0] # content.html
    
    for row in rows:
        cells = row.find_all('td')
        
        if len(cells) < 4: 
            continue 

        try:
            # --- 제목 및 링크 추출 (인덱스 1) ---
            title_tag = cells[1].find('a') 
            if not title_tag: continue
            
            title = title_tag.get_text(strip=True)
            
            # 링크: onclick="view(43653); return false;" 에서 고유 ID를 추출
            onclick_attr = title_tag.get('onclick')
            full_link = base_view_url
            
            if onclick_attr and 'view(' in onclick_attr:
                # 정규표현식을 사용하여 view() 안의 숫자(job_id) 추출
                match = re.search(r'view\((\d+)\)', onclick_attr)
                if match:
                    job_id = match.group(1)
                    # 상세 페이지 URL 조합 (pc=는 목록 페이지의 고유 ID)
                    # pc=는 하드코딩된 값이며, idx=는 동적으로 추출됩니다.
                    full_link = f"{base_view_url}?pc=SP5RQGKR3BAUE4W1XB8Q9IE8WF9WA4U&idx={job_id}"

            # --- 모집 기간 추출 및 변환 (인덱스 3) ---
            # cells[3]에 "2025.10.31 ~ 2025.11.14" 형식으로 날짜가 있음
            date_range_text = cells[3].get_text(strip=True)
            dates = date_range_text.split('~')
            
            if len(dates) == 2:
                # 날짜 형식 변환 (YYYY.MM.DD -> YYYY-MM-DD)
                start_date_str = dates[0].strip().replace('.', '-')
                end_date_str = dates[1].strip().replace('.', '-')
                
                # DB의 DATE 형식에 맞도록 파싱
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            else:
                start_date = date.today()
                end_date = date.today()
            
            # --- 데이터 모델에 맞게 저장 ---
            data.append({
                'company_name': site_name,
                # job_type은 현재 HTML 구조에서 추출이 어려우므로 제목 기반으로 임시 지정
                'job_type': '정규직' if '정규직' in title else ('인턴' if '인턴' in title else '계약직'),
                'title': title,
                'link': full_link,
                'start_date': start_date,
                'end_date': end_date,
            })

        except Exception as e:
            print(f"경고: 데이터 파싱 오류 발생 for row. 오류: {e}")
            continue

    return data

# ------------------------------------------------------------------
# 4. 메인 실행 블록
# ------------------------------------------------------------------
def run_crawler():
    db_generator = get_db()
    db = next(db_generator)
    total_new_postings_count = 0
    
    for site in JOB_SITES:
        site_name = site['name']
        base_url = site['url']
        print(f"\n--- INFO: {site_name} 크롤링 시작 ---")
        
        try:
            # 1. 실제 HTTP 요청
            response = requests.get(base_url, timeout=15, verify=False) 
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')

            # 2. 파싱 함수 호출
            parser_func = globals().get(site['parser'])
            if not parser_func: continue
            
            # 추출 함수 호출
            extracted_data = parser_func(soup, site_name, base_url) 
            
            # 3. 데이터베이스에 저장 (중복 방지 로직)
            new_postings = []
            for data in extracted_data:
                # 제목과 회사명을 기반으로 중복 검사
                exists = db.query(JobPosting).filter(
                    JobPosting.title == data['title'],
                    JobPosting.company_name == data['company_name']
                ).first()
                
                if not exists:
                    new_postings.append(JobPosting(**data))
                
            db.add_all(new_postings)
            db.commit()
            total_new_postings_count += len(new_postings)
            
            print(f"✅ SUCCESS: {site_name}에서 {len(new_postings)}개의 새 공고를 저장했습니다.")

        except requests.exceptions.RequestException as e:
            print(f"❌ ERROR: HTTP 요청 오류 발생 (URL 확인 또는 SSL 문제): {e}")
            
        except Exception as e:
            db.rollback()
            print(f"❌ ERROR: {site_name} 데이터 처리 중 오류 발생: {e}")
            
    db_generator.close()
    print(f"\n--- 최종 완료: 총 {total_new_postings_count}개의 새로운 공고가 저장되었습니다. ---")


if __name__ == "__main__":
    # DB 테이블이 없으면 생성
    Base.metadata.create_all(bind=engine)
    
    # 크롤러 실행
    run_crawler()