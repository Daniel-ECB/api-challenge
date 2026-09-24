from app.users.user_entity import UserEntity
from app.repositories.user_repository_base import UserRepositoryBase

class InMemoryUserRepository(UserRepositoryBase):
    def __init__(self) -> None:
        self._users: dict[int, UserEntity] = {}
        self._next_id = 1

    async def get_users_list(self) -> list[UserEntity]:
        return list(self._users.values())

    async def get_user_by_id(self, user_id: int) -> UserEntity | None:
        return self._users.get(user_id)

    async def get_user_by_email(self, email: str) -> UserEntity | None:
        normalized_email = email.lower()

        for user in self._users.values():
            if user.email.lower() == normalized_email:
                return user

        return None

    async def get_user_by_username(self, username: str) -> UserEntity | None:
        for user in self._users.values():
            if user.username.lower() == username.lower():
                return user

        return None

    async def create_user(self, username: str, email: str, password_hash: str) -> UserEntity:
        user = UserEntity(
            id=self._next_id,
            username=username,
            email=email.lower(),
            password_hash=password_hash,
        )

        self._users[user.id] = user
        self._next_id += 1
        return user

    async def update_user(self, user_update: UserEntity) -> UserEntity:
        self._users[user_update.id] = user_update
        return user_update

    async def delete_user(self, user_id: int) -> None:
        self._users.pop(user_id, None)