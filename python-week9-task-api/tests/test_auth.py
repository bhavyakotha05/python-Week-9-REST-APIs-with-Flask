import json


def test_register(client):
    response = client.post(
        "/api/auth/register",
        json={
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "password123"
        }
    )

    assert response.status_code == 201
    data = response.get_json()
    assert data["status"] == "success"
    assert "access_token" in data["data"]


def test_login(client):
    response = client.post(
        "/api/auth/login",
        json={
            "email": "testuser@example.com",
            "password": "password123"
        }
    )

    assert response.status_code == 200
    data = response.get_json()
    assert "access_token" in data["data"]
