from aiogram import types
from aiogram.utils.i18n import SimpleI18nMiddleware
from src.bot.repositories.user import UserRepository


class PostgresI18nMiddleware(SimpleI18nMiddleware):
    """
    Middleware that changes language based on user language stored in the database.
    """
    def __init__(self, i18n, user_repo: UserRepository = UserRepository()):
        super().__init__(i18n)
        self.user_repo = user_repo

    async def get_locale(self, event: types.TelegramObject, data: dict) -> str:
        """
        Get locale based on route's language stored in the database.
        """
        if not event:
            return self.i18n.default_locale

        user_id = event.from_user.id if hasattr(event, 'from_user') else None
        locale = None

        if user_id:
            user = await self.user_repo.get_by_telegram_id(telegram_id=user_id)
            locale = user.language if user else None
        if not locale:
            locale = await super().get_locale(event=event, data=data)
        return locale
