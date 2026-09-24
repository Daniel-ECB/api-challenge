from typing import Annotated
from fastapi import Depends
from app.repositories.in_memory_user_repository import InMemoryUserRepository
from app.repositories.user_repository_base import UserRepositoryBase
from app.users.user_service import UserService


user_repository = InMemoryUserRepository()


def get_user_repository() -> UserRepositoryBase:
    return user_repository


def get_user_service(repository: Annotated[UserRepositoryBase, Depends(get_user_repository)]) -> UserService:
    return UserService(user_repo=repository)