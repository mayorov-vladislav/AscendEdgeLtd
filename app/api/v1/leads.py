from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.lead_service import LeadService
from app.schemas.lead import *
from app.models.enums import ColdStage
from app.schemas.lead import LeadOut
from app.db.models.lead import Lead
from app.schemas.lead import LeadCreate
from sqlalchemy import select
from app.ai.lead_ai_service import LeadAIService
from app.repositories.lead_repository import LeadRepository


router = APIRouter(prefix="/leads", tags=["leads"])


@router.post("/")
async def create_lead(data: LeadCreate, db: AsyncSession = Depends(get_db)):
    lead = Lead(
        source=data.source,
        business_domain=data.business_domain,
    )
    db.add(lead)
    await db.commit()
    await db.refresh(lead)
    return lead

@router.patch("/{lead_id}/activity", response_model=LeadOut)
async def update_activity(
    lead_id: int,
    data: LeadActivityUpdate,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Lead).where(Lead.id == lead_id))
    lead = result.scalar_one_or_none()

    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    lead.activity = data.activity
    await db.commit()
    await db.refresh(lead)

    return LeadOut.model_validate(lead)


@router.post("/{lead_id}/transfer")
async def transfer(lead_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Lead).where(Lead.id == lead_id))
    lead = result.scalar_one()

    service = LeadService(db)
    return await service.transfer_to_sales(lead)

@router.patch("/{lead_id}/stage")
async def update_stage(
    lead_id: int,
    data: LeadStageUpdate,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Lead).where(Lead.id == lead_id))
    lead = result.scalar_one_or_none()

    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    service = LeadService(db)

    updated_lead = await service.update_stage(
        lead,
        ColdStage(data.stage),
    )

    return updated_lead

@router.post("/{lead_id}/analyze")
async def analyze_lead(lead_id: int, session: AsyncSession = Depends(get_db)):

    lead = await LeadRepository.get(session, lead_id)

    result = await LeadAIService.analyze(lead)

    lead.ai_score = result["score"]
    lead.ai_recommendation = result["recommendation"]

    await session.commit()

    return result