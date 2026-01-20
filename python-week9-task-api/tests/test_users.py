def test_get_current_user(client, auth_header):
    response = client.get("/api/users/me", headers=auth_header)

    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "success"
    assert "username" in data["data"]


def test_get_all_users(client, auth_header):
    response = client.get("/api/users", headers=auth_header)

    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data["data"], list)
