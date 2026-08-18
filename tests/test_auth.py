def test_health_check(client):
    response = client.get("/api/health")

    assert response.status_code == 200

    data = response.get_json()

    assert data["status"] == "success"


def test_register_user(client):
    response = client.post(
        "/api/auth/register",
        json={
            "username": "jitendra",
            "password": "password123"
        }
    )

    assert response.status_code == 201

    data = response.get_json()

    assert data["message"] == "User registered successfully"
    assert data["user"]["username"] == "jitendra"


def test_register_requires_username(client):
    response = client.post(
        "/api/auth/register",
        json={
            "password": "password123"
        }
    )

    assert response.status_code == 400


def test_register_requires_password(client):
    response = client.post(
        "/api/auth/register",
        json={
            "username": "jitendra"
        }
    )

    assert response.status_code == 400


def test_short_password_rejected(client):
    response = client.post(
        "/api/auth/register",
        json={
            "username": "jitendra",
            "password": "123"
        }
    )

    assert response.status_code == 400


def test_duplicate_username(client):

    client.post(
        "/api/auth/register",
        json={
            "username": "jitendra",
            "password": "password123"
        }
    )

    response = client.post(
        "/api/auth/register",
        json={
            "username": "jitendra",
            "password": "password123"
        }
    )

    assert response.status_code == 409


def test_login_success(client):

    client.post(
        "/api/auth/register",
        json={
            "username": "jitendra",
            "password": "password123"
        }
    )

    response = client.post(
        "/api/auth/login",
        json={
            "username": "jitendra",
            "password": "password123"
        }
    )

    assert response.status_code == 200

    data = response.get_json()

    assert "access_token" in data
    assert data["token_type"] == "Bearer"


def test_invalid_password(client):

    client.post(
        "/api/auth/register",
        json={
            "username": "jitendra",
            "password": "password123"
        }
    )

    response = client.post(
        "/api/auth/login",
        json={
            "username": "jitendra",
            "password": "wrongpassword"
        }
    )

    assert response.status_code == 401


def test_protected_endpoint_without_token(client):

    response = client.get("/api/auth/me")

    assert response.status_code == 401


def test_get_current_user(client, auth_token):

    response = client.get(
        "/api/auth/me",
        headers={
            "Authorization": f"Bearer {auth_token}"
        }
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["user"]["username"] == "testuser"