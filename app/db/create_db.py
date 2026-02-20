import asyncio
from app.db.models.lead import Base
from app.db.session import engine


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("База создана!")


asyncio.run(init_db())