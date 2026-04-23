
from fastapi import APIRouter, HTTPException, Depends
from backend import community_db
from backend.services import community_ai
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter(
    prefix="/community",
    tags=["community"]
)

class CommunityVote(BaseModel):
    rating: int
    comment: Optional[str] = None
    username: Optional[str] = "Anonymous"
    timestamp: str

class VoteRequest(BaseModel):
    barcode: str
    rating: int
    comment: Optional[str] = None
    username: str

class CommunityResponse(BaseModel):
    barcode: str
    average_rating: float
    total_reviews: int
    recent_reviews: List[CommunityVote]
    community_summary: str

@router.post("/vote")
async def submit_vote(vote: VoteRequest):
    community_db.save_vote(vote.barcode, vote.rating, vote.comment, vote.username)
    return {"message": "Vote submitted successfully"}

@router.get("/{barcode}", response_model=CommunityResponse)
async def get_community_data(barcode: str):
    # 1. Fetch data from DB
    counts = community_db.get_vote_counts(barcode)
    activity = community_db.get_product_activity(barcode, limit=20)
    
    # 2. Generate Consensus Summary
    comments = [a for a in activity if a.get('comment')]
    
    # Fallback summary if no comments yet
    summary = "No community reviews yet."
    if comments:
        # Pass dummy counts for now as AI expects old format, or just pass comments
        # Ideally update AI service too, but for now we focus on structure
        summary = community_ai.generate_consensus(barcode, counts, comments)

    # 3. Format Activity for Response
    formatted_activity = []
    for item in activity:
        formatted_activity.append(CommunityVote(
            rating=item.get('rating', 0),
            comment=item['comment'],
            username=item.get('username', 'Anonymous'),
            timestamp=item['timestamp']
        ))

    return CommunityResponse(
        barcode=barcode,
        average_rating=counts['average_rating'],
        total_reviews=counts['total_reviews'],
        recent_reviews=formatted_activity,
        community_summary=summary
    )
