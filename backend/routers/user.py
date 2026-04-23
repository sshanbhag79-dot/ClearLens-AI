from fastapi import APIRouter, HTTPException
from backend.models import UserProfile
import backend.user_db as user_db

router = APIRouter(prefix="/user", tags=["user"])

@router.on_event("startup")
def startup_event():
    user_db.init_db()

@router.get("/{username}", response_model=UserProfile)
async def get_profile(username: str):
    profile = user_db.get_user_profile(username)
    if profile:
        return UserProfile(
            allergies=profile.get("allergies", []),
            diets=profile.get("diets", []),
            strictness=profile.get("strictness", "Strict")
        )
    return UserProfile()

@router.post("/{username}")
async def update_profile(username: str, profile: UserProfile):
    success = user_db.update_user_profile(username, profile.dict())
    if not success:
        raise HTTPException(status_code=500, detail="Failed to update profile.")
    return {"message": "Profile updated successfully"}
