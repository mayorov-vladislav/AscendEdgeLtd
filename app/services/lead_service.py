from fastapi import HTTPException
from datetime import datetime, timedelta, timezone
from app.services.lead_state_machine import LeadStateMachine
from app.db.models.sale import Sale
from app.models.enums import *
from app.services.ai_service import AIService


class LeadService:

    def __init__(self, db):
        self.db = db
        self.ai_service = AIService()


    async def analyze_lead(self, lead):

        if not lead:
            raise HTTPException(status_code=404, detail="Lead not found")

        ai_result = await self.ai_service.analyze_lead(lead)

        lead.ai_score = ai_result.score
        lead.ai_recommendation = ai_result.recommendation
        lead.ai_reason = ai_result.reason
        lead.ai_analysis_count += 1
        lead.last_ai_analysis_at = datetime.now(timezone.utc)

        await self.db.commit()
        await self.db.refresh(lead)

        return {
            "score": lead.ai_score,
            "recommendation": lead.ai_recommendation,
            "reason": lead.ai_reason
        }

    async def update_stage(self, lead, new_stage):
        try:
            LeadStateMachine.validate_transition(lead.stage, new_stage)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

        if lead.stage in [ColdStage.transferred, ColdStage.lost]:
            raise HTTPException(
                status_code=400,
                detail="Cannot modify terminal stage"
            )

        lead.stage = new_stage
        await self.db.commit()
        await self.db.refresh(lead)
        return lead

    async def transfer_to_sales(self, lead):

        if not lead:
            raise HTTPException(status_code=404, detail="Lead not found")

        if lead.stage == ColdStage.transferred:
            raise HTTPException(
                status_code=400,
                detail="Lead already transferred"
            )

        if lead.stage == ColdStage.lost:
            raise HTTPException(
                status_code=400,
                detail="Lost leads cannot be transferred"
            )

        if not lead.business_domain:
            raise HTTPException(
                status_code=400,
                detail="Business domain required"
            )

        if lead.ai_score is None:
            raise HTTPException(
                status_code=400,
                detail="AI analysis required"
            )

        if lead.ai_score <= 0.6:
            raise HTTPException(
                status_code=400,
                detail="AI score too low for transfer"
            )

        if lead.ai_recommendation != AIRecommendation.transfer_to_sales:
            raise HTTPException(
                status_code=400,
                detail="AI does not recommend transfer"
            )

        sale = Sale(
            lead_id=lead.id,
            stage=SalesStage.new
        )

        self.db.add(sale)

        lead.stage = ColdStage.transferred

        await self.db.commit()
        await self.db.refresh(sale)

        return {
            "message": "Lead transferred to sales",
            "sale_id": sale.id
        }