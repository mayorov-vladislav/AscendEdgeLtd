from pydantic import BaseModel, ConfigDict
from typing import Optional
from app.models.enums import ColdStage, LeadSource, BusinessDomain


class LeadOut(BaseModel):
    id: int
    source: LeadSource
    stage: ColdStage
    business_domain: BusinessDomain
    activity: int
    ai_score: Optional[float]
    ai_recommendation: Optional[str]

    model_config = ConfigDict(from_attributes=True)