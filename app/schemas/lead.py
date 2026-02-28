from pydantic import BaseModel, ConfigDict
from typing import Optional
from app.models.enums import ColdStage, LeadSource, BusinessDomain, AIRecommendation
from datetime import datetime

class LeadCreate(BaseModel):
    source: LeadSource
    business_domain: Optional[BusinessDomain] = None

class LeadStageUpdate(BaseModel):
    stage: str


class LeadOut(BaseModel):
    id: int
    source: LeadSource
    stage: ColdStage
    business_domain: Optional[BusinessDomain]
    activity_count: int

    ai_score: Optional[float]
    ai_recommendation: Optional[AIRecommendation]
    ai_reason: Optional[str]
    ai_analysis_count: int
    last_ai_analysis_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)

class AIResponse(BaseModel):
    score: float
    recommendation: str
    reason: str

class LeadActivityUpdate(BaseModel):
    activity_count: int