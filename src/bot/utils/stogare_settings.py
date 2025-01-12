from functools import lru_cache
from typing import Union

from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage
from environs import Env
from pydantic.v1 import BaseSettings

from src.bot.core import config

env = Env()
env.read_env()


class StorageSettings(BaseSettings):
    user: str
    psswrd: str
    host: str
    port: int = 6379

    class Config:
        env_prefix = "REDIS_"

    @property
    def url(self) -> str:
        return f"redis://{self.user}:{self.psswrd}@{self.host}:{self.port}"

    @property
    def redis(self) -> Union[str, RedisStorage]:
        return RedisStorage.from_url(url=self.url)

    @property
    def get_storage(self):
        if config.USE_REDIS:
            return self.redis
        else:
            return MemoryStorage()


@lru_cache()
def get_storage_settings() -> StorageSettings:
    return StorageSettings()
