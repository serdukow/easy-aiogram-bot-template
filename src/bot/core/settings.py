from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from orjson import orjson

from src.bot import utils
from src.bot.utils.smart_sesion import SmartAiogramAiohttpSession


class BotSettings:

    @staticmethod
    def get_bot(token: str):
        aiogram_session_logger = utils.logging.setup_logger().bind(type="aiogram_session")
        session = SmartAiogramAiohttpSession(
            json_loads=orjson.loads,
            logger=aiogram_session_logger,
        )
        bot = Bot(token, default=DefaultBotProperties(parse_mode='HTML'), session=session)
        return bot
