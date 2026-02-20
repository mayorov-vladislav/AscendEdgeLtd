import asyncio
from app.db.session import AsyncSessionLocal
from app.db.models.lead import Lead
from app.repositories.lead_repository import LeadRepository
from app.services.lead_service import LeadService
from app.ai.lead_ai_service import LeadAIService


async def main():
    async with AsyncSessionLocal() as session:
        # Создание репозитория и сервисов
        repo = LeadRepository(session)
        lead_service = LeadService(repo)
        ai_service = LeadAIService()
        
        # Создание нового лида
        lead = await lead_service.create_lead(source="partner", business_domain="first")
        print(f"Создан лид: id={lead.id}, source={lead.source}, stage={lead.stage}")

        # Увеличение активности и обновление этапа
        lead.activity_count = 3
        await lead_service.update_stage(lead, 'contacted')
        print(f"Этап обновлён: id={lead.id}, stage={lead.stage}, activity_count={lead.activity_count}")

        # Запуск AI-анализа
        ai_result = await ai_service.analyze_lead(lead)
        print(f"AI-анализ: {ai_result}")

        # Проверка рекомендации AI для передачи в продажи
        if ai_result["recommendation"] == "transfer_to_sales":
            await lead_service.transfer_to_sales(lead)
            print(f"Лид передан в продажи: id={lead.id}, stage={lead.stage}")
        else:
            print(f"Лид остаётся на холодной стадии: id={lead.id}, stage={lead.stage}")

asyncio.run(main())
