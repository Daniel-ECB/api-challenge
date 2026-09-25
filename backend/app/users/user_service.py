from typing import List

from fastapi import HTTPException, status

from app.repositories.user_repository_base import UserRepositoryBase
from app.users.user_entity import UserEntity
from app.core.security import hash_password


class UserService:
    def __init__(self, user_repo: UserRepositoryBase):
        self.repository = user_repo


    async def get_users(self) -> List[UserEntity]:
        return await self.repository.get_users_list()


    async def get_user(self, user_id: int) -> UserEntity:
        user = await self.repository.get_user_by_id(user_id)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

        return user


    async def create_user(self, username: str, email: str, password: str) -> UserEntity:
        if await self.repository.get_user_by_email(email.lower()):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A user with this email already exists in the system.",
            )

        if await self.repository.get_user_by_username(username.lower()):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A user with this username already exists in the system.",
            )

        return await self.repository.create_user(
            username,
            email.lower(),
            hash_password(password)
        )


    async def update_user(self, user_id: int, username: str | None, email: str | None) -> UserEntity:
        user = await self.repository.get_user_by_id(user_id)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID {user_id} not found."
            )

        if username is not None and username.lower() != user.username.lower():
            existing_user = await self.repository.get_user_by_username(username.lower())

            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Username already exists",
                )

        if email is not None and email.lower() != user.email.lower():
            existing_user = await self.repository.get_user_by_email(email)

            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered",
                )

        if username is not None:
            user.username = username.lower()
        if email is not None:
            user.email = email.lower()

        await self.repository.update_user(user)

        return user


    async def delete_user(self, user_id: int) -> None:
        user = await self.repository.get_user_by_id(user_id)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID {user_id} not found."
            )

        await self.repository.delete_user(user_id)