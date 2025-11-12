# app/routers/update_postings.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.crawler import crawl_job_postings

router = APIRouter(prefix="/update-postings", tags=["Update Job Postings"])

@router.post("/")
def update_job_postings(db: Session = Depends(get_db)):
    """
    서버 내부용 API — 크롤러를 실행해 최신 공고를 DB에 저장합니다.
    """
    new_posts = crawl_job_postings(db)
    return {"status": "success", "new_posts_count": len(new_posts)}
