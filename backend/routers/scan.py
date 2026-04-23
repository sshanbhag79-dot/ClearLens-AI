from fastapi import APIRouter, HTTPException
from backend.models import ScanRequest, ScanResponse
from backend.services.open_food_facts import get_product_by_barcode
from backend.services.ai_analyzer import analyze_safety

router = APIRouter()

@router.post("/scan", response_model=ScanResponse)
async def scan_product(request: ScanRequest):
    # 1. Fetch Product Data
    if request.barcode:
        product = get_product_by_barcode(request.barcode)
    else:
        # TODO: Handle manual text or OCR input if implemented
        raise HTTPException(status_code=400, detail="Barcode required for MVP")
        
    if not product:
        raise HTTPException(status_code=404, detail="Product not found in Open Food Facts database.")
    
    if not product.ingredients_text:
         # Fallback if product exists but ingredients are missing
         # In a real app, we might prompt for OCR here
         pass

    # 2. AI Analysis
    analysis = analyze_safety(product, request.user_profile)
    # try:
    #     print(f"DEBUG: AI Analysis Result: {analysis.dict() if hasattr(analysis, 'dict') else analysis.model_dump()}")
    # except:
    #     pass
    
    return analysis
