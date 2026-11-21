from fastapi.testclient import TestClient
from app.main import app
import uuid


client = TestClient(app)


def create_account():
    email = f"contact-{uuid.uuid4().hex[:8]}@example.com"

    response = client.post(
        "/api/auth/register",
        json={
            "full_name": "Contact Test User",
            "email": email,
            "password": "TestPassword123",
            "workspace_name": "Contact Test Workspace",
            "business_type": "Technology"
        }
    )

    assert response.status_code == 201

    return response.json()


def test_contacts_require_authentication():
    response = client.get("/api/contacts/")

    assert response.status_code == 403


def test_create_and_list_contacts():
    account = create_account()

    headers = {
        "Authorization": f"Bearer {account['access_token']}"
    }

    creation = client.post(
        "/api/contacts/",
        headers=headers,
        json={
            "name": "John Kamau",
            "email": "john@example.com",
            "phone": "+254712345678",
            "company": "Example Ltd",
            "notes": "Potential customer"
        }
    )

    assert creation.status_code == 201
    assert creation.json()["name"] == "John Kamau"
    assert creation.json()["workspace_id"] == account["workspace_id"]

    listing = client.get(
        "/api/contacts/",
        headers=headers
    )

    assert listing.status_code == 200
    assert len(listing.json()) == 1
    assert listing.json()[0]["email"] == "john@example.com"


def test_contacts_are_workspace_isolated():
    account_one = create_account()
    account_two = create_account()

    headers_one = {
        "Authorization": f"Bearer {account_one['access_token']}"
    }

    headers_two = {
        "Authorization": f"Bearer {account_two['access_token']}"
    }

    client.post(
        "/api/contacts/",
        headers=headers_one,
        json={"name": "Private Business Contact"}
    )

    response = client.get(
        "/api/contacts/",
        headers=headers_two
    )

    assert response.status_code == 200
    assert response.json() == []
def test_edit_and_delete_contact():
    account = create_account()

    headers = {
        "Authorization": f"Bearer {account['access_token']}"
    }

    creation = client.post(
        "/api/contacts/",
        headers=headers,
        json={"name": "Original Contact"}
    )

    contact_id = creation.json()["id"]

    update = client.put(
        f"/api/contacts/{contact_id}",
        headers=headers,
        json={"name": "Updated Contact"}
    )

    assert update.status_code == 200
    assert update.json()["name"] == "Updated Contact"

    deletion = client.delete(
        f"/api/contacts/{contact_id}",
        headers=headers
    )

    assert deletion.status_code == 200

    listing = client.get("/api/contacts/", headers=headers)
    assert listing.json() == []


def test_cannot_edit_or_delete_another_workspace_contact():
    account_one = create_account()
    account_two = create_account()

    headers_one = {
        "Authorization": f"Bearer {account_one['access_token']}"
    }

    headers_two = {
        "Authorization": f"Bearer {account_two['access_token']}"
    }

    creation = client.post(
        "/api/contacts/",
        headers=headers_one,
        json={"name": "Private Contact"}
    )

    contact_id = creation.json()["id"]

    update = client.put(
        f"/api/contacts/{contact_id}",
        headers=headers_two,
        json={"name": "Unauthorized Change"}
    )

    assert update.status_code == 404

    deletion = client.delete(
        f"/api/contacts/{contact_id}",
        headers=headers_two
    )

    assert deletion.status_code == 404
