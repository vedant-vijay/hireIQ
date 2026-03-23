from fastapi import APIRouter, HTTPException
import schemas
from services.screening_graph import screening_app

router = APIRouter(prefix="/screening-graph", tags=["screening-graph"])

@router.post("/")
def run_screening_graph(screening: schemas.ScreeningResultCreate):
    result = screening_app.invoke({
        "job_id": screening.job_id,
        "candidate_id": screening.candidate_id,
        "job_description": "",
        "resume_text": "",
        "match_score": None,
        "reasoning": None,
        "recommendation": None
    })
    return {
        "match_score": result["match_score"],
        "reasoning": result["reasoning"],
        "recommendation": result["recommendation"]
    }