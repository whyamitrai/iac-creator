from fastapi import APIRouter
from pydantic import BaseModel
from backend.agent.graph import app as agent

router = APIRouter()

class QueryRequest(BaseModel):
    query: str

@router.post("/generate")
def generate_iac(request: QueryRequest):
    result = agent.invoke({"query": request.query})
    return {"output": result["output"]}