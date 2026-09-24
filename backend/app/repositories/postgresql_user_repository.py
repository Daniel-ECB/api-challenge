from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.user_repository_base import UserRepositoryBase
from app.users.user_entity import UserEntity
from app.users.user_model import UserModel


class PostgreSQLUserRepository(UserRepositoryBase):
    def __init__(self, db: AsyncSession) -> None:
        self._db = db


    @staticmethod
    def _to_entity(model: UserModel) -> UserEntity:
        return UserEntity(
            id=model.id,
            username=model.username,
            email=model.email,
            password_hash=model.password_hash,
        )


    async def get_users_list(self) -> list[UserEntity]:
        result = await self._db.execute(select(UserModel))
        users = result.scalars().all()
        user_entities: list[UserEntity] = []

        for user in users:
            entity = self._to_entity(user)
            user_entities.append(entity)

        return user_entities


    async def get_user_by_id(self, user_id: int) -> UserEntity | None:
        result = await self._db.execute(select(UserModel).where(UserModel.id == user_id))
        user = result.scalars().first()

        if user is None:
            return None

        return self._to_entity(user)


    async def get_user_by_email(self, email: str) -> UserEntity | None:
        result = await self._db.execute(select(UserModel).where(UserModel.email == email.lower()))
        user = result.scalars().first()

        if user is None:
            return None

        return self._to_entity(user)


    async def get_user_by_username(self, username: str) -> UserEntity | None:
        result = await self._db.execute(select(UserModel).where(UserModel.username == username.lower()))
        user = result.scalars().first()

        if user is None:
            return None

        return self._to_entity(user)


    async def create_user(self, username: str, email: str, password_hash: str) -> UserEntity:
        new_user = UserModel(
            username=username.lower(),
            email=email.lower(),
            password_hash=password_hash,
        )

        self._db.add(new_user)
        await self._db.commit()
        await self._db.refresh(new_user)
        return self._to_entity(new_user)


    async def update_user(self, user_update: UserEntity) -> UserEntity:
        result = await self._db.execute(select(UserModel).where(UserModel.id == user_update.id))
        user = result.scalars().first()

        if user is None:
            raise ValueError(f"User with id {user_update.id} not found")
        if user_update.username is not None:
            user.username = user_update.username.lower()
        if user_update.email is not None:
            user.email = user_update.email.lower()

        await self._db.commit()
        await self._db.refresh(user)
        return self._to_entity(user)


    async def delete_user(self, user_id: int) -> None:
        result = await self._db.execute(select(UserModel).where(UserModel.id == user_id))
        user = result.scalars().first()

        if user is None:
            raise ValueError(f"User with id {user_id} not found")

        await self._db.delete(user)
        await self._db.commit()