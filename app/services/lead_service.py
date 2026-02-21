from app.services.lead_state_machine import LeadStateMachine
from fastapi import HTTPException
from app.db.models.sale import Sale
from app.models.enums import *

class LeadService:

    def __init__(self, db):
        self.db = db

    async def update_stage(self, lead, new_stage):
        try:
            LeadStateMachine.validate_transition(lead.stage, new_stage)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

        lead.stage = new_stage
        await self.db.commit()
        await self.db.refresh(lead)
        return lead
    
    async def transfer_to_sales(self, lead):

        if not lead:
            raise HTTPException(status_code=404, detail="Lead not found")

        if lead.stage == ColdStage.transferred:
            raise HTTPException(status_code=400, detail="Lead already transferred")

        if lead.ai_score is None or lead.ai_score < 0.6:
            raise HTTPException(status_code=400, detail="Lead not ready for sales")

        if not lead.business_domain:
            raise HTTPException(status_code=400, detail="Business domain required")

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