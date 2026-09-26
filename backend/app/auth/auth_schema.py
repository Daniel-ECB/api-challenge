from pydantic import BaseModel

from app.users.user_schema import UserPrivate


class Token(BaseModel):
    access_token: str
    token_type: str

class AuthResponse(BaseModel):
    user: UserPrivate
    token: Token