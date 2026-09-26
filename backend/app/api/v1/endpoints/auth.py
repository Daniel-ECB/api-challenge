from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from app.api.dependencies import get_auth_service, get_user_service
from app.auth.auth_schema import Token, AuthResponse
from app.auth.auth_service import AuthService
from app.users.user_schema import UserCreate
from app.users.user_service import UserService

router = APIRouter()
UserServiceDependency = Annotated[UserService, Depends(get_user_service)]
AuthServiceDependency = Annotated[AuthService, Depends(get_auth_service)]

@router.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user_in: UserCreate, user_service: UserServiceDependency):
    """Register a new user in the system using user_service."""
    return await user_service.register_user(username=user_in.username, email=user_in.email, password=user_in.password)

@router.post("/token", response_model=Token)
async def login_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], auth_service: AuthServiceDependency):
    return await auth_service.login_for_access_token(email=form_data.username, password=form_data.password)