import pytest
from os import getenv
from convergent.db.models.books import bible_chapters
from convergent.db.repos.answer import AnswerRepo
from convergent.db.schemas.user import User
import json


@pytest.mark.asyncio
async def test_get_chapter_authenticated(client, db, populate_db):
    # Authenticate and get access token
    async with client as ac:
        login_response = await ac.post(
            "/login", json={"user_id": "user", "password": "password"}
        )
        access_token = login_response.json()["access_token"]

        # Make a request to the API endpoint with authentication headers
        response = await ac.get(
            "/chapter", headers={"Authorization": f"Bearer {access_token}"}
        )

    # Ensure that the response has a status code of 200
    assert response.status_code == 200

    # Ensure that the response contains the expected keys
    expected_keys = ["book", "chapter", "chapter_text"]
    assert all(key in response.json() for key in expected_keys)

    # Ensure that the selected book and chapter are valid
    selected_book = response.json()["book"]
    selected_chapter = response.json()["chapter"]
    assert selected_book in bible_chapters
    assert selected_chapter in range(1, bible_chapters[selected_book] + 1)

    # Bible is not completely inserted on ci so tests for content will fail


@pytest.mark.asyncio
async def test_register(client, db, populate_db):
    # Send a POST request to register the new user
    async with client as ac:
        response = await ac.post(
            "/register",
            json={"user_id": "test_user", "password": "pass", "partner_id": ""},
        )

    # Check that the response status code is 200
    assert response.status_code == 200

    # Check that the response message indicates the user was created
    assert response.json() == {"message": "test_user created."}


@pytest.mark.asyncio
async def test_get_has_answered(client, db, populate_db):
    # Send a POST request to the endpoint with the test user as the partner parameter
    async with client as ac:
        login_response = await ac.post(
            "/login", json={"user_id": "user", "password": "password"}
        )
        access_token = login_response.json()["access_token"]
        response = await ac.post(
            "/has_answered",
            json={"user_id": "user", "password": "password"},
            headers={"Authorization": f"Bearer {access_token}"},
        )

    # Check that the response status code is 200
    assert response.status_code == 200

    # Check that the response indicates that the user has been answered
    assert response.json() == {"answered": "False"}


@pytest.mark.asyncio
async def test_mark_answered_endpoint(client, db, populate_db):
    # Create a test user
    username = getenv("USERNAME")
    test_user = {
        "user_id": f"{username}",
        "password": "test_password",
        "partner_id": "test_partner_id",
    }

    # Make a request to the endpoint with the test user
    async with client as ac:
        login_response = await ac.post(
            "/login", json={"user_id": "user", "password": "password"}
        )
        access_token = login_response.json()["access_token"]
        response = await ac.post(
            "/answer",
            json=test_user,
            headers={"Authorization": f"Bearer {access_token}"},
        )
        get_has_answered_response = await client.post(
            "/has_answered",
            json=test_user,
            headers={"Authorization": f"Bearer {access_token}"},
        )

    # Verify that the response is successful
    assert response.status_code == 200

    # Verify that the response body contains the expected data
    assert response.json() == {"answered": "True"}

    # Verify that the get_has_answered response is successful
    assert get_has_answered_response.status_code == 200

    # Verify that the response body contains the expected data
    assert get_has_answered_response.json() == {"answered": "True"}
