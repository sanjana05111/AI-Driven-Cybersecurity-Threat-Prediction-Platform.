from fastapi import APIRouter
from pydantic import BaseModel
from app.services.ai_service import ai_service
from app.services.system_service import get_system_metrics
from app.schemas.chat import ChatRequest, ChatResponse

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest):
    sys = get_system_metrics()
    context = f"CPU: {sys['cpu']}%, RAM: {sys['memory']}%, NET: {sys['recv']}MB"
    response = ai_service.chat(request.message, context)
    return {"response": response}
