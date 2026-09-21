from typing import List

from fastapi import HTTPException, status

from app.users.user_repository import UserRepository
from app.users.user_schema import UserCreate, UserPrivate, UserPublic, UserUpdate
from app.users.user_model import User
from app.core.security import hash_password


class UserService:
    def __init__(self, user_repo: UserRepository):
        self.repository = user_repo


    async def get_users(self) -> List[User]:
        return self.repository.get_users_list()


    async def get_user(self, user_id: int) -> User:
        user = self.repository.get_user_by_id(user_id)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

        return user


    async def create_user(self, user_create: UserCreate) -> User:
        if self.repository.get_user_by_email(user_create.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A user with this email already exists in the system.",
            )

        new_user = User(
            username=user_create.username,
            email=user_create.email.lower(),
            password_hash=hash_password(user_create.password),
        )

        return self.repository.create_user(new_user.username, new_user.email, new_user.password_hash)


    async def update_user(self, user_id: int, user_update: UserUpdate) -> User:
        user = self.repository.get_user_by_id(user_id)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
            )

        if user_update.username is not None and user_update.username.lower() != user.username.lower():
            existing_user = self.repository.get_user_by_username(user_update.username)

            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Username already exists",
                )

        if user_update.email is not None and user_update.email.lower() != user.email.lower():
            existing_user = self.repository.get_user_by_email(user_update.email)

            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered",
                )

        if user_update.username is not None:
            user.username = user_update.username
        if user_update.email is not None:
            user.email = user_update.email.lower()

        self.repository.update_user(user)

        return user


    async def delete_user(self, user_id: int) -> None:
        user = self.repository.get_user_by_id(user_id)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID {user_id} not found."
            )

        self.repository.delete_user(user_id)


user_repository = UserRepository()
user_service = UserService(user_repo=user_repository)