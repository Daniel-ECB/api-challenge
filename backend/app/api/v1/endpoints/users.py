from fastapi import APIRouter, status
from app.users.user_schema import UserCreate, UserPrivate, UserPublic, UserUpdate
from app.users.user_repository import UserRepository

from app.users.user_service import user_service

router = APIRouter()

user_repository = UserRepository()

@router.get("/", response_model=list[UserPublic])
async def get_users():
    return await user_service.get_users()

@router.get("/{user_id}", response_model=UserPublic)
async def get_user(user_id: int):
    return await user_service.get_user(user_id=user_id)

@router.post("", response_model=UserPrivate, status_code=status.HTTP_201_CREATED)
async def create_user(user_in: UserCreate):
    return await user_service.create_user(user_create=user_in)

@router.patch("/{user_id}", response_model=UserPrivate)
async def update_user(user_id: int, user_in: UserUpdate):
    return await user_service.update_user(user_id=user_id, user_update=user_in)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int):
    return await user_service.delete_user(user_id=user_id)