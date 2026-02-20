from app.repositories.lead_repository import LeadRepository
from app.db.models.lead import Lead, LeadStage
from app.db.models.sale import Sale
from app.db.models.sale import SaleStage


ALLOWED_TRANSITIONS = {
    "new": ["contacted", "lost"],
    "contacted": ["qualified", "lost"],
    "qualified": ["transferred", "lost"],
}


class LeadService:
    def __init__(self, repo: LeadRepository):
        self.repo = repo

    async def create_lead(self, source: str, business_domain: str | None):
        lead = Lead(source=source, business_domain=business_domain)
        return await self.repo.create(lead)

    async def update_stage(self, lead: Lead, new_stage: str):

        if lead.stage == LeadStage.transferred:
            raise ValueError("Stage cannot be changed")

        current_stage = lead.stage.value

        if current_stage not in ALLOWED_TRANSITIONS:
            raise ValueError("Stage cannot be changed")

        if new_stage not in ALLOWED_TRANSITIONS[current_stage]:
            raise ValueError("Stage transition not allowed")

        lead.stage = LeadStage(new_stage)
        lead.activity_count += 3

        return await self.repo.update(lead)

    async def transfer_to_sales(self, lead: Lead):

        if lead.stage != LeadStage.qualified:
            raise ValueError("Lead must be qualified before transfer")

        if lead.ai_score is None:
            raise ValueError("AI analysis required before transfer")

        if lead.ai_score < 0.6:
            raise ValueError("AI score too low")

        if not lead.business_domain:
            raise ValueError("Business domain required")

        sale = Sale(
            lead_id=lead.id,
            stage=SaleStage.new
        )

        await self.repo.create_sale(sale)

        lead.stage = LeadStage.transferred

        return await self.repo.update(lead)