from sqlalchemy import Integer, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base
from app.models.enums import SalesStage


class Sale(Base):
    __tablename__ = "sales"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    lead_id: Mapped[int] = mapped_column(ForeignKey("leads.id"), nullable=False)
    stage: Mapped[SalesStage] = mapped_column(Enum(SalesStage), default=SalesStage.new)