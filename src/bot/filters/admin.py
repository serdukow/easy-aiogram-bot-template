from typing import Union

import structlog
from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery

from environs import Env

from src.bot.core import config

env = Env()
env.read_env()

logger = structlog.getLogger(__name__)


class AdminFilter(BaseFilter):
    async def __call__(self, obj: Union[Message, CallbackQuery]) -> bool:
        if obj.from_user.id in config.ADMINS_IDS:
            return True
        logger.warning(f"User {obj.from_user.id} is not listed among the admin IDs. "
                       f"You can add an admin by specifying their ID in the '.env' file.")
        return False
