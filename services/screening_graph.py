from typing import TypedDict, Optional
from database import SessionLocal
import models
from services import llm_services

class ScreeningState(TypedDict):
    job_id: int
    candidate_id: int
    job_description: str
    resume_text: str
    match_score: Optional[float]
    reasoning: Optional[str]
    recommendation: Optional[str]


def fetch_job(state: ScreeningState) -> dict:
    db = SessionLocal()
    try:
        job = db.query(models.Job).filter(
            models.Job.id == state["job_id"]
        ).first()
        return {"job_description": job.description}
    finally:
        db.close()
    
def fetch_candidates(state : ScreeningState) -> dict:
    db = SessionLocal()
    try:
        candidate = db.query(models.Candidate).filter(models.Candidate.id == state['candidate_id']).first()
        return {"resume_text" : candidate.resume_text}
    finally:
        db.close()



def screen_with_llm(state: ScreeningState) -> dict:
    result = llm_services.screen_candidate(
        state["job_description"],
        state["resume_text"]
    )
    return {
        "match_score": result["match_score"],
        "reasoning": result["reasoning"],
        "recommendation": result["recommendation"]
    }

def save_result(state: ScreeningState):
    db = SessionLocal()
    try:
        result = models.ScreeningResult(
            job_id=state["job_id"],
            candidate_id=state["candidate_id"],
            match_score=state["match_score"],
            reasoning=state["reasoning"],
            recommendation=state["recommendation"]
        )
        db.add(result)
        db.commit()
        db.refresh(result)
        return {}
    finally:
        db.close()

from langgraph.graph import StateGraph

def build_screening_graph():
    graph = StateGraph(ScreeningState)
    
    graph.add_node("fetch_job", fetch_job)
    graph.add_node("fetch_candidate", fetch_candidates)
    graph.add_node("screen_with_llm", screen_with_llm)
    graph.add_node("save_result", save_result)
    
    graph.set_entry_point("fetch_job")
    graph.add_edge("fetch_job", "fetch_candidate")
    graph.add_edge("fetch_candidate", "screen_with_llm")
    graph.add_edge("screen_with_llm", "save_result")
    graph.set_finish_point("save_result")
    
    return graph.compile()

screening_app = build_screening_graph()
    

