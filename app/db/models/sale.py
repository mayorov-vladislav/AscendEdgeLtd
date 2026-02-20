import enum
from sqlalchemy import Column, Integer, Enum, ForeignKey
from app.db.models.lead import Base


class SaleStage(str, enum.Enum):
    new = "new"
    kyc = "kyc"
    agreement = "agreement"
    paid = "paid"
    lost = "lost"


class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True)
    lead_id = Column(Integer, ForeignKey("leads.id"), nullable=False)

    stage = Column(Enum(SaleStage), default=SaleStage.new, nullable=False)