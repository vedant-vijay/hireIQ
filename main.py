from fastapi import FastAPI
from database import engine
import models
from routes import jobs, candidates

models.Base.metadata.create_all(bind=engine)
app = FastAPI()
app.include_router(jobs.router)
app.include_router(candidates.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}