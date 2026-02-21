from pydantic import BaseModel, ConfigDict
from app.models.enums import SalesStage

class SaleOut(BaseModel):
    id: int
    lead_id: int
    stage: SalesStage

    model_config = ConfigDict(from_attributes=True)

class SaleStageUpdate(BaseModel):
    stage: SalesStage