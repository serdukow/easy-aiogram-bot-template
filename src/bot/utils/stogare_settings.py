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
    def redis(self) -> RedisStorage:
        return RedisStorage.from_url(url=self.url)


@lru_cache()
def get_storage() -> Union[MemoryStorage, RedisStorage]:
    if config.USE_REDIS:
        redis_settings = StorageSettings()
        return redis_settings.redis
    else:
        return MemoryStorage()
