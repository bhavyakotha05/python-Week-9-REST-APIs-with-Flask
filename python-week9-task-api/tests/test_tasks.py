def test_create_task(client, auth_header):
    response = client.post(
        "/api/tasks",
        headers=auth_header,
        json={
            "title": "Test Task",
            "description": "Testing task creation",
            "priority": "high"
        }
    )

    assert response.status_code == 201
    data = response.get_json()
    assert data["status"] == "success"


def test_get_tasks(client, auth_header):
    response = client.get("/api/tasks", headers=auth_header)

    assert response.status_code == 200
    data = response.get_json()
    assert "tasks" in data["data"]


def test_update_task(client, auth_header):
    # Create task first
    create = client.post(
        "/api/tasks",
        headers=auth_header,
        json={"title": "Update Task"}
    )
    task_id = create.get_json()["data"]["task_id"]

    response = client.put(
        f"/api/tasks/{task_id}",
        headers=auth_header,
        json={"status": "completed"}
    )

    assert response.status_code == 200


def test_delete_task(client, auth_header):
    create = client.post(
        "/api/tasks",
        headers=auth_header,
        json={"title": "Delete Task"}
    )
    task_id = create.get_json()["data"]["task_id"]

    response = client.delete(
        f"/api/tasks/{task_id}",
        headers=auth_header
    )

    assert response.status_code == 204
