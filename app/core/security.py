import hashlib
import hmac
import secrets


ITERATIONS = 600_000


def hash_password(password: str) -> str:
    salt = secrets.token_hex(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        bytes.fromhex(salt),
        ITERATIONS
    )

    return f"pbkdf2_sha256${ITERATIONS}${salt}${password_hash.hex()}"


def verify_password(password: str, stored_hash: str) -> bool:
    try:
        algorithm, iterations, salt, expected_hash = stored_hash.split("$")

        if algorithm != "pbkdf2_sha256":
            return False

        iterations = int(iterations)

        if not 1 <= iterations <= ITERATIONS:
            return False

        actual_hash = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            bytes.fromhex(salt),
            iterations
        )

        return hmac.compare_digest(
            actual_hash.hex(),
            expected_hash
        )

    except (ValueError, TypeError):
        return False
from datetime import datetime, timedelta, timezone

import jwt

from app.core.config import settings


JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


def create_access_token(user_id: int) -> str:
    if not settings.SECRET_KEY or settings.SECRET_KEY == "replace-this-with-a-secure-secret":
        raise RuntimeError("A secure SECRET_KEY must be configured.")

    now = datetime.now(timezone.utc)

    payload = {
        "sub": str(user_id),
        "iat": now,
        "exp": now + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    }

    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=JWT_ALGORITHM
    )


def verify_access_token(token: str):
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[JWT_ALGORITHM]
        )

        user_id = payload.get("sub")

        if not user_id or not user_id.isdigit():
            return None

        return int(user_id)

    except (jwt.InvalidTokenError, AttributeError):
        return None
