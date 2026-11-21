import sqlite3

from app.database.connection import get_db
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token
)


def register_user(data):
    with get_db() as connection:
        try:
            cursor = connection.execute(
                """
                INSERT INTO workspaces (name, business_type)
                VALUES (?, ?)
                """,
                (data.workspace_name, data.business_type)
            )

            workspace_id = cursor.lastrowid

            cursor = connection.execute(
                """
                INSERT INTO users (
                    workspace_id,
                    full_name,
                    email,
                    password_hash
                )
                VALUES (?, ?, ?, ?)
                """,
                (
                    workspace_id,
                    data.full_name,
                    str(data.email).lower(),
                    hash_password(data.password)
                )
            )

            user_id = cursor.lastrowid

        except sqlite3.IntegrityError:
            raise ValueError("An account with this email already exists.")

    return {
        "access_token": create_access_token(user_id),
        "token_type": "bearer",
        "user_id": user_id,
        "workspace_id": workspace_id,
        "full_name": data.full_name,
        "email": str(data.email).lower()
    }


def login_user(data):
    with get_db() as connection:
        user = connection.execute(
            """
            SELECT *
            FROM users
            WHERE email = ?
            AND is_active = 1
            """,
            (str(data.email).lower(),)
        ).fetchone()

    if not user or not verify_password(
        data.password,
        user["password_hash"]
    ):
        raise ValueError("Invalid email or password.")

    return {
        "access_token": create_access_token(user["id"]),
        "token_type": "bearer",
        "user_id": user["id"],
        "workspace_id": user["workspace_id"],
        "full_name": user["full_name"],
        "email": user["email"]
    }
