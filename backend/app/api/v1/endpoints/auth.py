from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.api.dependencies import get_auth_service, get_current_user
from app.auth.auth_schema import Token
from app.auth.auth_service import AuthService
from app.users.user_entity import UserEntity
from app.users.user_schema import UserPrivate

router = APIRouter()
AuthServiceDependency = Annotated[AuthService, Depends(get_auth_service)]

@router.post("/token", response_model=Token)
async def login_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], auth_service: AuthServiceDependency):
    return await auth_service.login_for_access_token(email=form_data.username, password=form_data.password)

@router.get("/me", response_model=UserPrivate)
async def read_current_user(current_user: UserEntity = Depends(get_current_user)):
    return current_user