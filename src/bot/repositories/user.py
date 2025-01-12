from typing import Optional

import structlog

from src.bot.models.user import UserOrm
from src.bot.repositories.base import BaseRepository
from src.bot.utils.pg_session import get_pg_session


class UserRepository(BaseRepository):
    def __init__(self):
        super().__init__(UserOrm)
        self.logger = structlog.get_logger(__name__)

    async def create_user(self, **kwargs):
        """
        Create a new user in the database.

        :param kwargs: User data to create the user.
        :return: The created user instance.
        """
        async with get_pg_session() as session:
            try:
                user = UserOrm(**kwargs)
                await self.save(user)
                self.logger.info(f'User {user.telegram_id} created successfully')
                return user
            except Exception as e:
                await session.rollback()
                self.logger.error('Failed to create user, rolled back', detail=str(e))
                raise

    async def get_or_create_user(
        self,
        telegram_id: int,
        full_name: Optional[str],
        username: Optional[str] = None,
        is_premium: bool = False,
        is_bot: bool = False,
        language: Optional[str] = "en"
    ):
        """
        Get user or create a new one. Update user if data has changed.

        :param telegram_id: Telegram ID of the user.
        :param username: Username of the user.
        :param full_name: Full name of the user.
        :param is_premium: True if the user is a premium user.
        :param is_bot: True if the user is a bot.
        :param language: Language code (e.g., "ru", "en").
        :return: The user instance.
        """
        user = await self.get_by_telegram_id(telegram_id=telegram_id)
        if not user:
            user = await self.create_user(
                telegram_id=telegram_id,
                full_name=full_name,
                username=username,
                is_premium=is_premium,
                is_bot=is_bot,
                language=language
            )
            return user

        await self.fetch_telegram_updates(
            user=user,
            full_name=full_name,
            username=username,
            is_premium=is_premium,
            is_bot=is_bot,
            language=language
        )
        return user

    async def fetch_telegram_updates(
        self,
        user: UserOrm,
        full_name: Optional[str],
        username: Optional[str] = None,
        is_premium: bool = False,
        is_bot: bool = False,
        language: Optional[str] = "en"
    ):
        """
        Update an existing user's data if necessary. Example: when user change username or name.

        :param user: The existing user instance.
        :param full_name: New full name of the user.
        :param username: New username of the user.
        :param is_premium: True if the user is a premium user.
        :param is_bot: True if the user is a bot.
        :param language: New language code.
        :return: The updated user instance.
        """
        user_data = {
            "full_name": full_name,
            "username": username,
            "is_premium": is_premium,
            "is_bot": is_bot,
            "language": language,
        }

        updated_data = {key: value for key, value in user_data.items() if getattr(user, key) != value}
        if updated_data:
            self.logger.info(f'Updating user data with telegram id: {user.telegram_id}', updated_data=updated_data)
            await self.update(user.telegram_id, **updated_data)
        else:
            pass
        return user
