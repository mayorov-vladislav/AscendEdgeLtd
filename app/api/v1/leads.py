from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.services.lead_service import LeadService
from app.schemas.lead import *
from app.models.enums import ColdStage
from app.schemas.lead import LeadOut
from app.db.models.lead import Lead


router = APIRouter(prefix="/leads", tags=["leads"])


def get_lead_service(db: AsyncSession = Depends(get_db)):
    return LeadService(db)


@router.get("/{lead_id}", response_model=LeadOut)
async def get_lead(
    lead_id: int,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Lead).where(Lead.id == lead_id)
    )
    lead = result.scalar_one_or_none()

    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    return lead

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

    lead.activity_count = data.activity_count

    await db.commit()
    await db.refresh(lead)

    return LeadOut.model_validate(lead)


@router.patch("/{lead_id}/stage")
async def update_stage(
    lead_id: int,
    data: LeadStageUpdate,
    service: LeadService = Depends(get_lead_service),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Lead).where(Lead.id == lead_id))
    lead = result.scalar_one_or_none()

    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    updated_lead = await service.update_stage(
        lead,
        ColdStage(data.stage),
    )

    return updated_lead


@router.post("/{lead_id}/analyze")
async def analyze_lead(
    lead_id: int,
    service: LeadService = Depends(get_lead_service),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Lead).where(Lead.id == lead_id))
    lead = result.scalar_one_or_none()

    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    return await service.analyze_lead(lead)


@router.post("/{lead_id}/transfer")
async def transfer(
    lead_id: int,
    service: LeadService = Depends(get_lead_service),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Lead).where(Lead.id == lead_id))
    lead = result.scalar_one_or_none()

    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    return await service.transfer_to_sales(lead)