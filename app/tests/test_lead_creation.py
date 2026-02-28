import pytest

@pytest.mark.asyncio
async def test_create_lead(client):
    response = await client.post(
        "/api/v1/leads/",
        json={"source": "manual", "business_domain": "first"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["stage"] == "new"
    assert data["activity_count"] == 0


@pytest.mark.asyncio
async def test_update_activity(client):
    create = await client.post(
        "/api/v1/leads/",
        json={"source": "manual", "business_domain": "first"}
    )
    lead_id = create.json()["id"]

    response = await client.patch(
        f"/api/v1/leads/{lead_id}/activity",
        json={"activity_count": 10}
    )

    assert response.status_code == 200
    assert response.json()["activity_count"] == 10