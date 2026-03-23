from fastapi import FastAPI
from database import engine
import models
from routes import jobs, candidates, screening
from fastapi.middleware.cors import CORSMiddleware
from routes import screening_graph_route


models.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(jobs.router)
app.include_router(candidates.router)
app.include_router(screening.router)
app.include_router(screening_graph_route.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}