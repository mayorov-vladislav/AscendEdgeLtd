from pydantic import BaseModel, field_validator
from typing import Literal
from enum import Enum



class AIRecommendation(str, Enum):
    TRANSFER = "transfer_to_sales"
    NURTURE = "keep_nurturing"
    LOST = "mark_as_lost"


class AIResponse(BaseModel):
    score: float
    recommendation: AIRecommendation
    reason: str | None = None

    @field_validator("score")
    @classmethod
    def validate_score(cls, v):
        if not 0 <= v <= 1:
            raise ValueError("Score must be between 0 and 1")
        return v