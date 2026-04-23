from fastapi import APIRouter, HTTPException
from backend.models import ChatRequest, ChatResponse
from backend.services.bio_guide import get_bio_guide_reply
from backend.services.open_food_facts import get_product_by_barcode

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("/bio-guide", response_model=ChatResponse)
async def chat_with_bio_guide(request: ChatRequest):
    """
    Handles conversational interaction with the Bio-Guide AI.
    """
    current_product = None
    if request.barcode:
        current_product = get_product_by_barcode(request.barcode)
    
    try:
        reply = get_bio_guide_reply(request, current_product)
        return reply
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
