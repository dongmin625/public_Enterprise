from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/postings", tags=["Job Postings"])

# 모든 공고 조회
@router.get("/", response_model=list[schemas.JobPostingResponse])
def get_postings(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    postings = db.query(models.JobPosting).offset(skip).limit(limit).all()
    return postings

# 공고 등록
@router.post("/", response_model=schemas.JobPostingResponse)
def create_posting(posting: schemas.JobPostingCreate, db: Session = Depends(get_db)):
    db_posting = models.JobPosting(**posting.dict())
    db.add(db_posting)
    db.commit()
    db.refresh(db_posting)
    return db_posting
