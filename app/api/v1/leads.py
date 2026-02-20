from fastapi import APIRouter, HTTPException, Depends
from typing import AsyncGenerator
from app.schemas.lead import LeadCreate, LeadStageUpdate, AIResponse
from app.repositories.lead_repository import LeadRepository
from app.services.lead_service import LeadService
from app.ai.lead_ai_service import LeadAIService
from app.db.session import AsyncSessionLocal

router = APIRouter()
ai_service = LeadAIService()


async def get_repo() -> AsyncGenerator[LeadRepository, None]:
    async with AsyncSessionLocal() as session:
        yield LeadRepository(session)


@router.post("/", response_model=dict)
async def create_lead(
    lead_in: LeadCreate,
    repo: LeadRepository = Depends(get_repo)
):
    service = LeadService(repo)
    lead = await service.create_lead(
        lead_in.source,
        lead_in.business_domain
    )

    return {"id": lead.id, "stage": lead.stage}


@router.patch("/{lead_id}/stage", response_model=dict)
async def update_stage(
    lead_id: int,
    stage_update: LeadStageUpdate,
    repo: LeadRepository = Depends(get_repo)
):
    service = LeadService(repo)
    lead = await repo.get_by_id(lead_id)

    if not lead:
        raise HTTPException(404, "Lead not found")

    try:
        lead = await service.update_stage(lead, stage_update.new_stage)
    except ValueError as e:
        raise HTTPException(400, str(e))

    return {"id": lead.id, "stage": lead.stage}


@router.get("/{lead_id}/ai", response_model=AIResponse)
async def ai_analysis(
    lead_id: int,
    repo: LeadRepository = Depends(get_repo)
):
    lead = await repo.get_by_id(lead_id)

    if not lead:
        raise HTTPException(404, "Lead not found")

    ai_result = await ai_service.analyze_lead(lead)

    lead.ai_score = ai_result["score"]
    lead.ai_recommendation = ai_result["recommendation"]

    await repo.update(lead)

    return ai_result


@router.post("/{lead_id}/transfer", response_model=dict)
async def transfer_to_sales(
    lead_id: int,
    repo: LeadRepository = Depends(get_repo)
):
    service = LeadService(repo)
    lead = await repo.get_by_id(lead_id)

    if not lead:
        raise HTTPException(404, "Lead not found")

    try:
        lead = await service.transfer_to_sales(lead)
    except ValueError as e:
        raise HTTPException(400, str(e))

    return {"id": lead.id, "stage": lead.stage}