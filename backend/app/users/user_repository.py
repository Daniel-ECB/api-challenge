from app.users.user_dto import User

class UserRepository:
    def __init__(self) -> None:
        self._users: dict[int, User] = {}
        self._next_id = 1

    def get_users_list(self) -> list[User]:
        return list(self._users.values())

    def get_user_by_id(self, user_id: int) -> User | None:
        return self._users.get(user_id)

    def get_user_by_email(self, email: str) -> User | None:
        normalized_email = email.lower()

        for user in self._users.values():
            if user.email.lower() == normalized_email:
                return user

        return None

    def get_user_by_username(self, username: str) -> User | None:
        for user in self._users.values():
            if user.username.lower() == username.lower():
                return user

        return None

    def create_user(self, username: str, email: str, password_hash: str) -> User:
        user = User(
            id=self._next_id,
            username=username,
            email=email.lower(),
            password_hash=password_hash,
        )

        self._users[user.id] = user
        self._next_id += 1
        return user

    def update_user(self, user: User) -> None:
        self._users[user.id] = user


    def delete_user(self, user_id: int) -> bool:
        return self._users.pop(user_id, None) is not None