import pytest
from httpx import AsyncClient
from os import getenv


@pytest.mark.asyncio
async def test_login_success(db, populate_db, client: AsyncClient):
    username = getenv("USERNAME")
    password = getenv("PASSWORD")
    async with client as ac:
        response = await ac.post(
            url="/login",
            content='{{"user_id": "{}","password": "{}"}}'.format(username, password),
        )
    response_json = response.json()
    assert "error" not in response_json.keys()


@pytest.mark.asyncio
async def test_login_failure(db, populate_db, client: AsyncClient):
    username = getenv("USERNAME")
    password = getenv("PASSWORD")

    async with client as ac:
        response = await ac.post(
            url="/login",
            content='{{"user_id": "{}","password": "{}lol"}}'.format(
                username, password
            ),
        )
    response_json = response.json()
    assert "error" in response_json.keys()
