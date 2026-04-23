from typing import List, Optional
from pydantic import BaseModel

class UserProfile(BaseModel):
    allergies: List[str] = []
    diets: List[str] = []
    strictness: str = "Strict"  # Strict or Flexible

class ProductData(BaseModel):
    code: str
    product_name: str
    ingredients_text: str
    image_url: Optional[str] = None
    nutriscore: Optional[str] = None
    calories: Optional[float] = None  # kcal per 100g/ml
    quantity_val: Optional[float] = None # numeric quantity (e.g. 330)
    quantity_unit: Optional[str] = None # unit (e.g. ml, g)
    marketing_claims: Optional[str] = None # e.g. "Low Fat", "Natural"

class ScanRequest(BaseModel):
    barcode: Optional[str] = None
    manual_code: Optional[str] = None
    user_profile: UserProfile

class IngredientAnalysis(BaseModel):
    name: str
    status: str  # Safe, Caution, Avoid
    reason: str
    significance: str  # High, Medium, Low, Trace or Ultra-Trace

class ScanResponse(BaseModel):
    status: str  # Green, Yellow, Red
    reason: str
    alternative: Optional[str] = None
    product: ProductData
    pros: List[str] = []
    cons: List[str] = []
    health_score: Optional[int] = None
    ingredients_analysis: List[IngredientAnalysis] = []
    marketing_vs_reality: Optional[str] = None
    community_takeaway: Optional[str] = None
    bio_red_flags: List[str] = []
    trust_score: Optional[int] = None

class LogMealRequest(BaseModel):
    username: str
    barcode: str
    product_name: str
    calories: Optional[float] = 0.0
    quantity: float = 1.0
    status: str = "Yellow"
    total_calories: Optional[float] = None # Explicit override

class ChatRequest(BaseModel):
    message: str
    username: str
    barcode: Optional[str] = None # Current context
    user_profile: UserProfile

class ChatResponse(BaseModel):
    reply: str
    intent: Optional[str] = None # e.g. "LOG_MEAL"
    log_params: Optional[dict] = None # Data to trigger save_to_daily_log
