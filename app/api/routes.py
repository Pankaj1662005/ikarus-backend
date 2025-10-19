from fastapi import APIRouter
from pydantic import BaseModel
from app.api.recommender_raw import get_raw_recommendations

router = APIRouter()

class RecommendRequest(BaseModel):
    prompt: str

@router.post("/recommend/raw")
def recommend_raw(data: RecommendRequest):
    resp = get_raw_recommendations(data.prompt)
    return {"results": resp}
