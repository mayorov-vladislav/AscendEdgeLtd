from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.models.lead import Lead
from app.db.models.sale import Sale


class LeadRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, lead: Lead):
        self.session.add(lead)
        await self.session.commit()
        await self.session.refresh(lead)
        return lead

    async def get(self, lead_id: int):
        result = await self.session.execute(
            select(Lead).where(Lead.id == lead_id)
        )
        return result.scalar_one_or_none()

    async def list(self):
        result = await self.session.execute(select(Lead))
        return result.scalars().all()

    async def update(self, lead: Lead):
        self.session.add(lead)
        await self.session.commit()
        await self.session.refresh(lead)
        return lead

    async def get_by_id(self, lead_id: int):
        return await self.get(lead_id)

    async def create_sale(self, sale: Sale):
        self.session.add(sale)
        await self.session.commit()
        await self.session.refresh(sale)
        return sale