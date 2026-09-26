from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from app.auth.auth_service import AuthService
from app.db.database import AsyncSession, get_db
from app.repositories.postgresql_user_repository import PostgreSQLUserRepository
from app.repositories.user_repository_base import UserRepositoryBase
from app.users.user_entity import UserEntity
from app.users.user_service import UserService


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")


def get_user_repository(db: AsyncSession = Depends(get_db)) -> UserRepositoryBase:
    return PostgreSQLUserRepository(db)

def get_user_service(repository: Annotated[UserRepositoryBase, Depends(get_user_repository)]) -> UserService:
    return UserService(user_repo=repository)

def get_auth_service(repository: Annotated[UserRepositoryBase, Depends(get_user_repository)]) -> AuthService:
    return AuthService(user_repo=repository)

async def get_current_user(
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    token: str = Depends(oauth2_scheme)
) -> UserEntity:
    """Extract the HTTP token and delegate the validation to the service."""
    return await auth_service.get_user_from_token(token=token)