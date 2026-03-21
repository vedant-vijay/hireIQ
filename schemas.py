from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# INPUT — what recruiter sends when creating a job
class JobCreate(BaseModel):
    title: str
    description: str

# OUTPUT — what API sends back
class JobResponse(BaseModel):
    id: int
    title: str
    description: str
    created_at: datetime

    class Config:
        from_attributes = True

class CandidateCreate(BaseModel):
    name: str
    email: str
    resume_text: str
    job_id: int

class CandidateResponse(BaseModel):
    id: int
    name: str
    email: str
    job_id: int

    class Config:
        from_attributes = True

class ScreeningResultCreate(BaseModel):
    job_id: int
    candidate_id: int

class ScreenResultResponse(BaseModel):
    id: int
    match_score: float
    reasoning: str
    recommendation: str
    created_at: datetime

    class Config:
        from_attributes = True