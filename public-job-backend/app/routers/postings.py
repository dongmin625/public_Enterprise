from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
# Firebase 인증 의존성 함수 임포트
from app.dependencies import get_current_user_uid 
from typing import Annotated

router = APIRouter(prefix="/postings", tags=["Job Postings"])

# 공고 조회 (로그인 필수)
@router.get("/", response_model=list[schemas.JobPostingResponse])
def get_postings(
    # [인증 인자] 필수 인자이므로, 기본값(Depends)을 가진 인자들보다 앞에 위치해야 합니다.
    # Firebase 토큰 검증에 성공하면, current_user_uid에 사용자의 UID가 할당됩니다.
    current_user_uid: Annotated[str, Depends(get_current_user_uid)], 
    
    # [DB 세션 인자] 기본값을 가지므로, 인증 인자 뒤에 위치합니다.
    db: Session = Depends(get_db), 
    
    # [쿼리 파라미터] 기본값을 가지므로, 가장 뒤에 위치합니다.
    skip: int = 0, 
    limit: int = 20, 
):
    """
    인증된 사용자에게만 크롤링된 공고 목록을 제공합니다.
    로그인하지 않았거나 토큰이 유효하지 않으면 401 Unauthorized 오류가 발생합니다.
    """
    
    print(f"DEBUG: 공고 조회 성공! 사용자 UID: {current_user_uid}") 
    
    # SQLAlchemy를 사용하여 DB에서 공고 데이터를 조회
    postings = db.query(models.JobPosting).offset(skip).limit(limit).all()
    
    return postings

# (공고 등록 POST 라우터는 크롤링 시스템용이므로 일반 사용자 백엔드에서는 제외되었습니다.)