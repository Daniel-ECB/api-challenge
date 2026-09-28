from datetime import timedelta
from typing import List

from fastapi import HTTPException, status

from app.clients.poke_api import PokeAPIClient
from app.core.config import settings
from app.repositories.user_repository_base import UserRepositoryBase
from app.users.user_entity import UserEntity
from app.core.security import hash_password, create_access_token
from app.users.user_schema import UserPrivate, UserPublic


class UserService:
    def __init__(self, user_repo: UserRepositoryBase, pokemon_client: PokeAPIClient):
        self.repository = user_repo
        self.pokemon_client = pokemon_client

    async def get_current_user_profile(self, user: UserEntity) -> UserPrivate:
        pokemon_names = await self.pokemon_client.get_pokemon_names_by_ids(user.pokemon_team)

        return UserPrivate(
            id=user.id,
            username=user.username,
            email=user.email,
            pokemon_team=pokemon_names,
        )

    async def get_users(self) -> List[UserPublic]:
        users = await self.repository.get_users_list()
        users_with_pokemon = []

        for user in users:
            pokemon_names = await self.pokemon_client.get_pokemon_names_by_ids(user.pokemon_team or [])
            user = UserPublic(
                id=user.id,
                username=user.username,
                pokemon_team=pokemon_names
            )

            users_with_pokemon.append(user)

        return users_with_pokemon


    async def get_user(self, user_id: int) -> UserPublic:
        user = await self.repository.get_user_by_id(user_id)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

        pokemon_names = await self.pokemon_client.get_pokemon_names_by_ids(user.pokemon_team or [])

        return UserPublic(
            id=user.id,
            username=user.username,
            pokemon_team=pokemon_names
        )


    async def register_user(self, username: str, email: str, password: str, pokemon_team: list[int]) -> dict:
        user = await self.create_user(username, email, password, pokemon_team)

        access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
        access_token = create_access_token(
            data={"sub": str(user.id)}, expires_delta=access_token_expires
        )

        return {
            "user": user,
            "token": {"access_token": access_token, "token_type": "bearer"}
        }


    async def create_user(self, username: str, email: str, password: str, pokemon_team: list[int]) -> UserPrivate:
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

        user_entity = await self.repository.create_user(
            username,
            email.lower(),
            hash_password(password),
            pokemon_team
        )

        pokemon_names = await self.pokemon_client.get_pokemon_names_by_ids(pokemon_team or [])

        return UserPrivate(
            id=user_entity.id,
            email=user_entity.email,
            username=user_entity.username,
            pokemon_team=pokemon_names
        )


    async def update_user(
            self,
            current_user_id: int,
            user_id: int,
            username: str | None,
            email: str | None,
            pokemon_team: list[int] | None
    ) -> UserPrivate:
        if user_id != current_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to update this user",
            )

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
        if pokemon_team is not None:
            user.pokemon_team = pokemon_team

        user_entity = await self.repository.update_user(user)

        pokemon_names = await self.pokemon_client.get_pokemon_names_by_ids(user.pokemon_team)

        return UserPrivate(
            id=user_entity.id,
            email=user_entity.email,
            username=user_entity.username,
            pokemon_team=pokemon_names
        )


    async def delete_user(self, current_user_id: int, user_id: int) -> None:
        if user_id != current_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to delete this user",
            )

        user = await self.repository.get_user_by_id(user_id)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID {user_id} not found."
            )

        await self.repository.delete_user(user_id)