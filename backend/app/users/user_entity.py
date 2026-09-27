from dataclasses import dataclass, field


@dataclass
class UserEntity:
    id: int
    username: str
    email: str
    password_hash: str
    pokemon_team: list[int] = field(default_factory=list)