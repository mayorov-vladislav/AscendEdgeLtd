import enum
from sqlalchemy import Column, Integer, String, Float, Enum
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class LeadStage(str, enum.Enum):
    new = "new"
    contacted = "contacted"
    qualified = "qualified"
    transferred = "transferred"
    lost = "lost"


class LeadSource(str, enum.Enum):
    scanner = "scanner"
    partner = "partner"
    manual = "manual"


class BusinessDomain(str, enum.Enum):
    first = "first"
    second = "second"
    third = "third"


class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    source = Column(Enum(LeadSource), nullable=False)
    stage = Column(Enum(LeadStage), default=LeadStage.new, nullable=False)
    business_domain = Column(Enum(BusinessDomain), nullable=True)
    activity_count = Column(Integer, default=0)

    ai_score = Column(Float, nullable=True)
    ai_recommendation = Column(String, nullable=True)