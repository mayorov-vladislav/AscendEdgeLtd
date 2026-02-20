from pydantic import BaseModel
from typing import Optional
from app.db.models.lead import LeadStage, LeadSource, BusinessDomain


class LeadCreate(BaseModel):
    source: LeadSource
    business_domain: Optional[BusinessDomain] = None

class LeadStageUpdate(BaseModel):
    new_stage: LeadStage

class LeadOut(BaseModel):
    id: int
    source: str
    stage: str
    business_domain: Optional[str] = None
    activity_count: int
    ai_score: Optional[float] = None
    ai_recommendation: Optional[str] = None

    class Config:
        orm_mode = True

class AIResponse(BaseModel):
    score: float
    recommendation: str
    reason: str