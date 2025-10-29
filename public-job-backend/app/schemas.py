from pydantic import BaseModel
from typing import Optional
from datetime import date

# 사용자 관련 스키마
class UserCreate(BaseModel):
    email: str
    password: str
    nickname: Optional[str]

class UserResponse(BaseModel):
    id: int
    email: str
    nickname: Optional[str]

    class Config:
        orm_mode = True

# 채용 공고 관련 스키마
class JobPostingCreate(BaseModel):
    company_name: str
    job_type: str
    title: str
    link: str
    start_date: Optional[date]
    end_date: Optional[date]

class JobPostingResponse(BaseModel):
    id: int
    company_name: str
    job_type: str
    title: str
    link: str
    start_date: Optional[date]
    end_date: Optional[date]

    class Config:
        orm_mode = True
