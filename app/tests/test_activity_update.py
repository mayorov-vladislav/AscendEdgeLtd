import pytest

@pytest.mark.asyncio
async def test_activity_update(client):
    response = await client.post(
        "/api/v1/leads/",
        json={"source": "scanner", "business_domain": "first"}
    )
    lead_id = response.json()["id"]

    response = await client.patch(
        f"/api/v1/leads/{lead_id}/activity",
        json={"activity": 5}
    )

    assert response.status_code == 200
    assert response.json()["activity"] == 5