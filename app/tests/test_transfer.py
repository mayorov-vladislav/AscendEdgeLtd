import pytest
from app.services.ai_service import AIService

class FakeAIService:
    async def analyze_lead(self, lead):
        return type("AIResult", (), {
            "score": 0.8,
            "recommendation": "transfer_to_sales",
            "reason": "High engagement"
        })()


@pytest.mark.asyncio
async def test_full_pipeline(client, monkeypatch):

    monkeypatch.setattr(
        "app.services.lead_service.AIService",
        lambda: FakeAIService()
    )

    create = await client.post(
        "/api/v1/leads/",
        json={"source": "manual", "business_domain": "first"}
    )
    lead_id = create.json()["id"]

    await client.patch(
        f"/api/v1/leads/{lead_id}/activity",
        json={"activity_count": 15}
    )

    analyze = await client.post(
        f"/api/v1/leads/{lead_id}/analyze"
    )

    assert analyze.status_code == 200
    assert analyze.json()["recommendation"] == "transfer_to_sales"

    transfer = await client.post(
        f"/api/v1/leads/{lead_id}/transfer"
    )

    assert transfer.status_code == 200
    assert transfer.json()["message"] == "Lead transferred to sales"

    second_transfer = await client.post(
        f"/api/v1/leads/{lead_id}/transfer"
    )

    assert second_transfer.status_code == 400


@pytest.mark.asyncio
async def test_transfer_blocked_low_score(client, monkeypatch):

    class LowScoreAI:
        async def analyze_lead(self, lead):
            return type("AIResult", (), {
                "score": 0.4,
                "recommendation": "keep_nurturing",
                "reason": "Low engagement"
            })()

    monkeypatch.setattr(
        "app.services.lead_service.AIService",
        lambda: LowScoreAI()
    )

    create = await client.post(
        "/api/v1/leads/",
        json={"source": "manual", "business_domain": "first"}
    )
    lead_id = create.json()["id"]

    await client.patch(
        f"/api/v1/leads/{lead_id}/activity",
        json={"activity_count": 3}
    )

    await client.post(f"/api/v1/leads/{lead_id}/analyze")

    transfer = await client.post(
        f"/api/v1/leads/{lead_id}/transfer"
    )

    assert transfer.status_code == 400