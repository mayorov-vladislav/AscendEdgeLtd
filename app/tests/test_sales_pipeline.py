import pytest
from sqlalchemy import select
from app.db.models.lead import Lead
from app.models.enums import AIRecommendation


@pytest.mark.asyncio
async def test_sales_stage_transition(client, db_session):
    response = await client.post(
        "/api/v1/leads/",
        json={"source": "scanner", "business_domain": "first"}
    )
    lead_id = response.json()["id"]

    await client.patch(f"/api/v1/leads/{lead_id}/stage", json={"stage": "contacted"})
    await client.patch(f"/api/v1/leads/{lead_id}/stage", json={"stage": "qualified"})

    result = await db_session.execute(select(Lead).where(Lead.id == lead_id))
    lead = result.scalar_one()

    lead.ai_score = 0.95
    lead.ai_recommendation = AIRecommendation.transfer_to_sales
    await db_session.commit()

    response = await client.post(f"/api/v1/leads/{lead_id}/transfer")
    assert response.status_code == 200

    sale_id = response.json()["sale_id"]

    response = await client.patch(
        f"/api/v1/sales/{sale_id}/stage",
        json={"stage": "kyc"}
    )

    assert response.status_code == 200
    assert response.json()["stage"] == "kyc"