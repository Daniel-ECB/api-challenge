from typing import Annotated
from fastapi import APIRouter, Depends, status

from app.users.user_schema import UserCreate, UserPrivate, UserPublic, UserUpdate
from app.api.dependencies import get_user_service
from app.users.user_service import UserService

router = APIRouter()
UserServiceDependency = Annotated[UserService, Depends(get_user_service)]

@router.get("", response_model=list[UserPublic])
async def get_users(user_service: UserServiceDependency):
    return await user_service.get_users()

@router.get("/{user_id}", response_model=UserPublic)
async def get_user(user_id: int, user_service: UserServiceDependency):
    return await user_service.get_user(user_id=user_id)

@router.post("", response_model=UserPrivate, status_code=status.HTTP_201_CREATED)
async def create_user(user_in: UserCreate, user_service: UserServiceDependency):
    return await user_service.create_user(username=user_in.username, email=user_in.email, password=user_in.password)

@router.patch("/{user_id}", response_model=UserPrivate)
async def update_user(user_id: int, user_in: UserUpdate, user_service: UserServiceDependency):
    return await user_service.update_user(user_id=user_id, username=user_in.username, email=user_in.email)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, user_service: UserServiceDependency):
    return await user_service.delete_user(user_id=user_id)