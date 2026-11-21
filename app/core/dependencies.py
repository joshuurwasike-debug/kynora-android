from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.core.security import verify_access_token
from app.database.connection import get_db


bearer_scheme = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
):
    user_id = verify_access_token(credentials.credentials)

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired authentication token."
        )

    with get_db() as connection:
        user = connection.execute(
            """
            SELECT id, workspace_id, full_name, email, role, is_active
            FROM users
            WHERE id = ?
            """,
            (user_id,)
        ).fetchone()

    if user is None or not user["is_active"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User account is unavailable."
        )

    return dict(user)
def get_current_workspace(
    current_user: dict = Depends(get_current_user)
):
    return current_user["workspace_id"]
