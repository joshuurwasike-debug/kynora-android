from fastapi import APIRouter, HTTPException, status, Depends

from app.schemas.auth import (
    RegisterRequest,
    LoginRequest,
    AuthResponse
)

from app.services.auth_service import register_user, login_user
from app.core.dependencies import get_current_user
router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post(
    "/register",
    response_model=AuthResponse,
    status_code=status.HTTP_201_CREATED
)
def register(data: RegisterRequest):
    try:
        return register_user(data)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error)
        )


@router.post("/login", response_model=AuthResponse)
def login(data: LoginRequest):
    try:
        return login_user(data)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(error)
        )
@router.get("/me")
def read_current_user(
    current_user: dict = Depends(get_current_user)
):
    return current_user
