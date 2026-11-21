from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "operational"


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_register_and_login():
    import uuid

    email = f"test-{uuid.uuid4().hex[:8]}@example.com"

    registration = client.post(
        "/api/auth/register",
        json={
            "full_name": "API Test User",
            "email": email,
            "password": "TestPassword123",
            "workspace_name": "API Test Workspace",
            "business_type": "Technology"
        }
    )

    assert registration.status_code == 201

    login = client.post(
        "/api/auth/login",
        json={
            "email": email,
            "password": "TestPassword123"
        }
    )

    assert login.status_code == 200
    assert login.json()["access_token"]
    assert login.json()["workspace_id"] > 0


def test_invalid_login():
    response = client.post(
        "/api/auth/login",
        json={
            "email": "unknown@example.com",
            "password": "WrongPassword123"
        }
    )

    assert response.status_code == 401
def test_current_user_requires_authentication():
    response = client.get("/api/auth/me")

    assert response.status_code == 403


def test_current_user_with_valid_token():
    import uuid

    email = f"me-{uuid.uuid4().hex[:8]}@example.com"

    registration = client.post(
        "/api/auth/register",
        json={
            "full_name": "Current User Test",
            "email": email,
            "password": "TestPassword123",
            "workspace_name": "Current User Workspace",
            "business_type": "Technology"
        }
    )

    assert registration.status_code == 201

    token = registration.json()["access_token"]

    response = client.get(
        "/api/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert response.json()["email"] == email
    assert response.json()["full_name"] == "Current User Test"
    assert "password_hash" not in response.json()
def test_current_user_workspace_isolation():
    import uuid

    email = f"workspace-{uuid.uuid4().hex[:8]}@example.com"

    registration = client.post(
        "/api/auth/register",
        json={
            "full_name": "Workspace Test User",
            "email": email,
            "password": "TestPassword123",
            "workspace_name": "Private Workspace",
            "business_type": "Technology"
        }
    )

    assert registration.status_code == 201

    data = registration.json()

    response = client.get(
        "/api/auth/me",
        headers={
            "Authorization": f"Bearer {data['access_token']}"
        }
    )

    assert response.status_code == 200
    assert response.json()["workspace_id"] == data["workspace_id"]
