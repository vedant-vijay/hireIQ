from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models, schemas
from services import llm_services

router = APIRouter(prefix="/screening", tags=["screening"])

@router.post("/", response_model=schemas.ScreenResultResponse)
def screening_result(screening: schemas.ScreeningResultCreate, db:Session = Depends(get_db)):
    
    db_job = db.query(models.Job).filter(models.Job.id == screening.job_id).first()
    db_candidate = db.query(models.Candidate).filter(models.Candidate.id == screening.candidate_id).first()
    if not db_job or not db_candidate:
        raise HTTPException(status_code=404, detail="not found")
    
    db_screening_results = llm_services.screen_candidate(db_job.description, db_candidate.resume_text)
    db_screening = models.ScreeningResult(job_id=screening.job_id, candidate_id = screening.candidate_id, match_score = db_screening_results['match_score'], reasoning = db_screening_results['reasoning'], recommendation = db_screening_results['recommendation'])
    db.add(db_screening)
    db.commit()
    db.refresh(db_screening)
    return db_screening

@router.get("/rankings/{job_id}", response_model=list[schemas.ScreenResultResponse])
def get_rankings(job_id: int, db: Session = Depends(get_db)):
    db_job = db.query(models.Job).filter(models.Job.id == job_id).first()
    if not db_job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    results = db.query(models.ScreeningResult)\
        .filter(models.ScreeningResult.job_id == job_id)\
        .order_by(models.ScreeningResult.match_score.desc())\
        .all()
    
    return results