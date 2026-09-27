from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    secret_key: SecretStr
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    postgres_user: str
    postgres_password: SecretStr
    postgres_server: str = "localhost"
    postgres_port: int = 5432
    postgres_db: str

    pokeapi_base_url: str

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+psycopg://"
            f"{self.postgres_user}:"
            f"{self.postgres_password.get_secret_value()}@"
            f"{self.postgres_server}:{self.postgres_port}/"
            f"{self.postgres_db}"
        )

settings = Settings()