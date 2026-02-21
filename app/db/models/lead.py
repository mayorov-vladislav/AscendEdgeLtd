from sqlalchemy import Integer, Enum, Float
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base
from app.models.enums import LeadSource, BusinessDomain, ColdStage, AIRecommendation


class Lead(Base):
    __tablename__ = "leads"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    source: Mapped[LeadSource] = mapped_column(Enum(LeadSource), nullable=False)
    stage: Mapped[ColdStage] = mapped_column(Enum(ColdStage), default=ColdStage.new)

    business_domain: Mapped[BusinessDomain | None] = mapped_column(
        Enum(BusinessDomain), nullable=True
    )

    activity_count: Mapped[int] = mapped_column(Integer, default=0)

    ai_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    ai_recommendation: Mapped[AIRecommendation | None] = mapped_column(
        Enum(AIRecommendation), nullable=True
    )