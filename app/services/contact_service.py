from app.schemas.contacts import ContactCreate, ContactUpdate
from app.database.connection import get_db
from app.schemas.contacts import ContactCreate


def create_contact(data: ContactCreate, workspace_id: int):
    with get_db() as connection:
        cursor = connection.execute(
            """
            INSERT INTO contacts (
                workspace_id,
                name,
                email,
                phone,
                company,
                notes
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                workspace_id,
                data.name,
                str(data.email) if data.email else None,
                data.phone,
                data.company,
                data.notes
            )
        )

        contact = connection.execute(
            """
            SELECT *
            FROM contacts
            WHERE id = ? AND workspace_id = ?
            """,
            (cursor.lastrowid, workspace_id)
        ).fetchone()

        return dict(contact)


def get_contacts(workspace_id: int):
    with get_db() as connection:
        contacts = connection.execute(
            """
            SELECT *
            FROM contacts
            WHERE workspace_id = ?
            ORDER BY created_at DESC, id DESC
            """,
            (workspace_id,)
        ).fetchall()

        return [dict(contact) for contact in contacts]
def update_contact(
    contact_id: int,
    workspace_id: int,
    data: ContactUpdate
):
    updates = data.dict(exclude_unset=True)

    allowed_fields = {
        "name", "email", "phone", "company", "notes"
    }

    if not updates or not set(updates).issubset(allowed_fields):
        return None

    if "email" in updates and updates["email"] is not None:
        updates["email"] = str(updates["email"])

    fields = ", ".join(f"{field} = ?" for field in updates)

    values = list(updates.values())
    values.extend([contact_id, workspace_id])

    with get_db() as connection:
        cursor = connection.execute(
            f"""
            UPDATE contacts
            SET {fields}, updated_at = CURRENT_TIMESTAMP
            WHERE id = ? AND workspace_id = ?
            """,
            values
        )

        if cursor.rowcount == 0:
            return None

        contact = connection.execute(
            """
            SELECT *
            FROM contacts
            WHERE id = ? AND workspace_id = ?
            """,
            (contact_id, workspace_id)
        ).fetchone()

        return dict(contact)


def delete_contact(contact_id: int, workspace_id: int):
    with get_db() as connection:
        cursor = connection.execute(
            """
            DELETE FROM contacts
            WHERE id = ? AND workspace_id = ?
            """,
            (contact_id, workspace_id)
        )

        return cursor.rowcount > 0
