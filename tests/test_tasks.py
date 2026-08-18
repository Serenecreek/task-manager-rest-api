def auth_headers(token):
    return {
        "Authorization": f"Bearer {token}"
    }


def test_create_task(client, auth_token):

    response = client.post(
        "/api/tasks",
        headers=auth_headers(auth_token),
        json={
            "title": "Learn Flask",
            "description": "Build a REST API"
        }
    )

    assert response.status_code == 201

    data = response.get_json()

    assert data["task"]["title"] == "Learn Flask"
    assert data["task"]["completed"] is False


def test_create_task_requires_authentication(client):

    response = client.post(
        "/api/tasks",
        json={
            "title": "Learn Flask"
        }
    )

    assert response.status_code == 401


def test_create_task_requires_title(client, auth_token):

    response = client.post(
        "/api/tasks",
        headers=auth_headers(auth_token),
        json={
            "description": "No title"
        }
    )

    assert response.status_code == 400


def test_get_tasks(client, auth_token):

    client.post(
        "/api/tasks",
        headers=auth_headers(auth_token),
        json={
            "title": "Task 1"
        }
    )

    client.post(
        "/api/tasks",
        headers=auth_headers(auth_token),
        json={
            "title": "Task 2"
        }
    )

    response = client.get(
        "/api/tasks",
        headers=auth_headers(auth_token)
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["count"] == 2
    assert len(data["tasks"]) == 2


def test_get_single_task(client, auth_token):

    create_response = client.post(
        "/api/tasks",
        headers=auth_headers(auth_token),
        json={
            "title": "Learn SQL"
        }
    )

    task_id = create_response.get_json()["task"]["id"]

    response = client.get(
        f"/api/tasks/{task_id}",
        headers=auth_headers(auth_token)
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["task"]["title"] == "Learn SQL"


def test_update_task(client, auth_token):

    create_response = client.post(
        "/api/tasks",
        headers=auth_headers(auth_token),
        json={
            "title": "Learn Flask"
        }
    )

    task_id = create_response.get_json()["task"]["id"]

    response = client.put(
        f"/api/tasks/{task_id}",
        headers=auth_headers(auth_token),
        json={
            "title": "Master Flask",
            "completed": True
        }
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["task"]["title"] == "Master Flask"
    assert data["task"]["completed"] is True


def test_delete_task(client, auth_token):

    create_response = client.post(
        "/api/tasks",
        headers=auth_headers(auth_token),
        json={
            "title": "Temporary task"
        }
    )

    task_id = create_response.get_json()["task"]["id"]

    response = client.delete(
        f"/api/tasks/{task_id}",
        headers=auth_headers(auth_token)
    )

    assert response.status_code == 200

    get_response = client.get(
        f"/api/tasks/{task_id}",
        headers=auth_headers(auth_token)
    )

    assert get_response.status_code == 404


def test_nonexistent_task(client, auth_token):

    response = client.get(
        "/api/tasks/99999",
        headers=auth_headers(auth_token)
    )

    assert response.status_code == 404


def test_user_cannot_access_another_users_task(client, auth_token):

    # User 1 creates a task
    create_response = client.post(
        "/api/tasks",
        headers=auth_headers(auth_token),
        json={
            "title": "Private task"
        }
    )

    task_id = create_response.get_json()["task"]["id"]

    # Create User 2
    client.post(
        "/api/auth/register",
        json={
            "username": "seconduser",
            "password": "password123"
        }
    )

    login_response = client.post(
        "/api/auth/login",
        json={
            "username": "seconduser",
            "password": "password123"
        }
    )

    second_token = login_response.get_json()["access_token"]

    # User 2 attempts to access User 1's task
    response = client.get(
        f"/api/tasks/{task_id}",
        headers=auth_headers(second_token)
    )

    assert response.status_code == 404