from fastapi import APIRouter, HTTPException
from backend.models import LogMealRequest
import backend.daily_log_db as daily_log_db

router = APIRouter(prefix="/log", tags=["log"])

@router.on_event("startup")
def startup_event():
    daily_log_db.init_db()

@router.post("/meal")
async def log_meal_endpoint(request: LogMealRequest):
    success = daily_log_db.log_meal(
        request.username,
        request.barcode,
        product_name=request.product_name,
        calories_per_100g=request.calories,
        quantity=request.quantity,
        status=request.status,
        total_calories=request.total_calories
    )
    if not success:
        raise HTTPException(status_code=500, detail="Failed to log meal.")
    return {"message": "Meal logged successfully"}

@router.get("/summary/{username}")
async def get_summary_endpoint(username: str):
    summary = daily_log_db.get_daily_summary(username)
    return summary

@router.get("/history/{username}")
async def get_history_endpoint(username: str):
    logs = daily_log_db.get_daily_logs(username)
    return logs

@router.delete("/{log_id}")
async def delete_log_endpoint(log_id: int):
    success = daily_log_db.delete_log(log_id)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to delete log.")
    return {"message": "Log deleted successfully"}
