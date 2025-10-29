from sqlalchemy import Column, Integer, String, Text, DateTime, Date
from sqlalchemy.sql import func
from app.database import Base

# 사용자 계정 테이블
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    nickname = Column(String(50))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

# 채용 공고 테이블
class JobPosting(Base):
    __tablename__ = "job_postings"

    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String(255))
    job_type = Column(String(50))   # 정규직, 인턴 등
    title = Column(String(255))
    link = Column(Text)
    start_date = Column(Date)
    end_date = Column(Date)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
