from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
import datetime

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    candidates = relationship("Candidate", back_populates="job")
    screeningresults = relationship("ScreeningResult", back_populates = "job")

class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key = True, index = True)
    name = Column(String, nullable = False)
    email = Column(String, nullable = False)
    resume_text = Column(String, nullable = False)
    job_id = Column(Integer, ForeignKey("jobs.id"))

    job = relationship("Job", back_populates = "candidates")
    screeningresults = relationship("ScreeningResult", back_populates = "candidate")

class ScreeningResult(Base):
    __tablename__ = "screeningresults"

    id = Column(Integer, primary_key = True, index = True)
    match_score = Column(Float, nullable = False)
    reasoning = Column(String, nullable = False)
    recommendation = Column(String, nullable = False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    job_id = Column(Integer, ForeignKey("jobs.id"))
    candidate_id = Column(Integer, ForeignKey('candidates.id'))

    job = relationship("Job", back_populates = "screeningresults")
    candidate = relationship("Candidate", back_populates = "screeningresults")