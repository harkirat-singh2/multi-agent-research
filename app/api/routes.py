from fastapi import APIRouter
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
from app.pipeline.research_pipeline import run_research_stream



router = APIRouter()

class Request(BaseModel):
    query: str

@router.post("/research")
def research(req: Request):
    return run_research_pipeline(req.query)
  
  
@router.get("/research/stream")
def stream_research(query: str):
    return StreamingResponse(
        run_research_stream(query),
        media_type="text/plain"
    )  