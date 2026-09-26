from datetime import timedelta

from fastapi import HTTPException, status

from app.repositories.user_repository_base import UserRepositoryBase
from app.core.security import create_access_token, verify_password, verify_access_token
from app.core.config import settings
from app.users.user_entity import UserEntity


class AuthService:
    def __init__(self, user_repo: UserRepositoryBase):
        self.user_repository = user_repo

    @staticmethod
    def _credentials_exception():
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


    async def login_for_access_token(self, email: str, password: str) -> dict:
        user = await self.user_repository.get_user_by_email(email.lower())

        if not user or not verify_password(password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Create access token with user id as subject
        access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
        access_token = create_access_token(
            data={"sub": str(user.id)},
            expires_delta=access_token_expires,
        )

        return {"access_token": access_token, "token_type": "bearer"}


    async def get_user_from_token(self, token: str) -> UserEntity:
        subject = verify_access_token(token)

        if subject is None:
            raise self._credentials_exception()

        try:
            user_id = int(subject)
        except (ValueError, TypeError):
            raise self._credentials_exception()

        user = await self.user_repository.get_user_by_id(user_id=user_id)
        if not user:
            raise self._credentials_exception()

        return user