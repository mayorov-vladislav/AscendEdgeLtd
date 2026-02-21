import pytest

@pytest.mark.asyncio
async def test_create_lead(client):
    response = await client.post(
        "/api/v1/leads/",
        json={
            "source": "scanner",
            "business_domain": "first"
        }
    )

    assert response.status_code == 200
    data = response.json()

    assert data["source"] == "scanner"
    assert data["stage"] == "new"