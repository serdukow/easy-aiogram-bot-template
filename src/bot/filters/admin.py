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
    """
    AdminFilter is a custom filter used to verify if a user is listed among the admin IDs.

    This filter checks whether the `from_user.id` of an incoming `Message` or `CallbackQuery`
    matches any of the IDs specified in the `ADMINS_IDS` configuration.

    Behavior:
        - Returns `True` if the user is an admin (their ID is in `ADMINS_IDS`).
        - Logs a warning and returns `False` if the user is not an admin.

    Logging:
        If a non-admin user triggers this filter, a warning is logged with their user ID.
        It also includes a suggestion to add the user's ID to the `.env` file to grant them admin rights.

    Example:
        @router.message(AdminFilter()) or @router.callback_query(AdminFilter())
        async def handle_admin_message(message: Message):
            await message.answer("Welcome, admin!")

    Returns:
        bool: Whether the user is an admin.
    """
    async def __call__(self, obj: Union[Message, CallbackQuery]) -> bool:
        """

        :param obj: incoming update to filter.
        :return: True if user is admin.
        """
        if obj.from_user.id in config.ADMINS_IDS:
            return True
        logger.warning(
            f"User {obj.from_user.id} is not listed among the admin IDs. "
            f"You can add an admin by specifying their ID in the '.env' file."
        )
        return False
