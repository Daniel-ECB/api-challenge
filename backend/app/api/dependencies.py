from typing import Annotated
from fastapi import Depends

from app.db.database import AsyncSession, get_db
from app.repositories.postgresql_user_repository import PostgreSQLUserRepository
from app.repositories.user_repository_base import UserRepositoryBase
from app.users.user_service import UserService


def get_user_repository(db: AsyncSession = Depends(get_db)) -> UserRepositoryBase:
    return PostgreSQLUserRepository(db)


def get_user_service(repository: Annotated[UserRepositoryBase, Depends(get_user_repository)]) -> UserService:
    return UserService(user_repo=repository)