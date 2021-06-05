import pytest


@pytest.mark.asyncio
async def test_index(default_client):
    r = await default_client.get("")
    assert r.status_code == 200
