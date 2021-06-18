import pytest


@pytest.mark.asyncio
async def test_get_empty_user(client):
    r = await client.get("/users")

    assert r.status_code == 200


@pytest.mark.asyncio
async def test_get_user(client, add_user):
    user = add_user()
    r = await client.get("/users")
    data = r.json()

    assert r.status_code == 200
    assert isinstance(data, list)
    assert data[0].get("username") == user.username
