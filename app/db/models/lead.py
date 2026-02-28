from datetime import datetime
from sqlalchemy import Integer, Enum, Float, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base
from app.models.enums import LeadSource, BusinessDomain, ColdStage, AIRecommendation


class Lead(Base):
    __tablename__ = "leads"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    source: Mapped[LeadSource] = mapped_column(Enum(LeadSource), nullable=False)
    stage: Mapped[ColdStage] = mapped_column(
        Enum(ColdStage),
        default=ColdStage.new
    )

    business_domain: Mapped[BusinessDomain | None] = mapped_column(
        Enum(BusinessDomain),
        nullable=True
    )

    activity_count: Mapped[int] = mapped_column(Integer, default=0)

    ai_score: Mapped[float | None] = mapped_column(Float, nullable=True)

    ai_recommendation: Mapped[AIRecommendation | None] = mapped_column(
        Enum(AIRecommendation),
        nullable=True
    )

    ai_reason: Mapped[str | None] = mapped_column(String, nullable=True)

    ai_analysis_count: Mapped[int] = mapped_column(Integer, default=0)

    last_ai_analysis_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )