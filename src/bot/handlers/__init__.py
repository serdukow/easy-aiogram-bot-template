from aiogram import Dispatcher

from src.bot.handlers.start_handler import router
from src.bot.handlers.is_member import router as member_router


def register_handlers(dp: Dispatcher):
    dp.include_router(router)
    dp.include_router(member_router)
