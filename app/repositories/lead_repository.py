from sqlalchemy import select
from app.db.models.lead import Lead


class LeadRepository:

    @staticmethod
    async def get(session, lead_id: int):
        result = await session.execute(
            select(Lead).where(Lead.id == lead_id)
        )
        return result.scalar_one_or_none()