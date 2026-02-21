from pydantic import BaseModel, ConfigDict
from typing import Optional
from app.models.enums import ColdStage, LeadSource, BusinessDomain

class LeadCreate(BaseModel):
    source: LeadSource
    business_domain: Optional[BusinessDomain] = None

class LeadStageUpdate(BaseModel):
    stage: str

class LeadOut(BaseModel):
    id: int
    source: LeadSource
    stage: ColdStage
    business_domain: BusinessDomain
    activity: int
    ai_score: Optional[float]
    ai_recommendation: Optional[str]
    activity_count: int 

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def model_validate(cls, obj):
        if not hasattr(obj, "activity_count"):
            obj.activity_count = obj.activity
        return super().model_validate(obj)

class AIResponse(BaseModel):
    score: float
    recommendation: str
    reason: str

class LeadActivityUpdate(BaseModel):
    activity: int