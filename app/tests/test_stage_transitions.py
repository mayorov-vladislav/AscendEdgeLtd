import pytest

@pytest.mark.asyncio
async def test_valid_stage_transition(client):
    response = await client.post(
        "/api/v1/leads/",
        json={"source": "scanner", "business_domain": "first"}
    )
    lead_id = response.json()["id"]

    response = await client.patch(
        f"/api/v1/leads/{lead_id}/stage",
        json={"stage": "contacted"}
    )

    assert response.status_code == 200
    assert response.json()["stage"] == "contacted"


@pytest.mark.asyncio
async def test_invalid_stage_transition(client):
    response = await client.post(
        "/api/v1/leads/",
        json={"source": "scanner", "business_domain": "first"}
    )
    lead_id = response.json()["id"]

    response = await client.patch(
        f"/api/v1/leads/{lead_id}/stage",
        json={"stage": "qualified"}
    )

    assert response.status_code == 400