from functools import lru_cache

from environs import Env
from pydantic.v1 import BaseSettings

env = Env()
env.read_env()


class PostgresSettings(BaseSettings):
    name: str
    user: str
    psswrd: str
    host: str
    port: int = 5432

    class Config:
        env_prefix = "PG_"

    @property
    def url(self) -> str:
        return f"postgresql://{self.user}:{self.psswrd}@{self.host}:{self.port}/{self.name}"

    @property
    def async_url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.psswrd}@{self.host}:{self.port}/{self.name}"


@lru_cache()
def get_pg_settings() -> PostgresSettings:
    return PostgresSettings()
