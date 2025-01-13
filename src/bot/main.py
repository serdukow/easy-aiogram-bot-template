import uvicorn

from fastapi import FastAPI, status

import asyncio

from contextlib import asynccontextmanager

import structlog

from typing import AsyncIterator

from aiogram import Dispatcher, Bot, types
from aiogram.utils.callback_answer import CallbackAnswerMiddleware

from src.server.controllers import register_controllers

from src.bot.core import config
from src.bot.handlers import register_handlers
from src.bot.middlewares.PostgresI18nMiddleware import PostgresI18nMiddleware
from src.bot.middlewares.logging import StructLoggingMiddleware
from src.bot.models import async_create_tables
from src.bot import utils
from src.bot.core.settings import BotSettings
from src.bot.utils.stogare_settings import get_storage
from src.bot.utils.localization import get_i18n
from src.bot.utils.pg_session import engine
from src.bot.utils.webhook_settings import get_webhook_settings

logger = structlog.get_logger(__name__)

dp = Dispatcher(
    storage=get_storage(),
    maintenance_mode=config.MAINTENANCE_MODE)

bot = BotSettings().get_bot(config.BOT_TOKEN)


def setup_middlewares(dp: Dispatcher) -> None:
    PostgresI18nMiddleware(get_i18n()).setup(dp)
    dp.update.outer_middleware(StructLoggingMiddleware(logger=dp["aiogram_logger"]))
    dp.update.middleware(CallbackAnswerMiddleware())


def setup_logging(dp: Dispatcher) -> None:
    dp['aiogram_logger'] = utils.logging.setup_logger().bind(type='aiogram')
    dp['db_logger'] = utils.logging.setup_logger().bind(type='db')
    dp['cache_logger'] = utils.logging.setup_logger().bind(type='cache')
    dp['business_logger'] = utils.logging.setup_logger().bind(type='business')


async def setup_aiogram(dp: Dispatcher) -> None:
    register_handlers(dp=dp)
    await async_create_tables(engine)
    setup_logging(dp)
    logger = dp['aiogram_logger']
    logger.debug('Configuring aiogram')
    setup_middlewares(dp)
    logger.info('Configured aiogram')


async def aiogram_on_startup_polling(dispatcher: Dispatcher, bot: Bot) -> None:
    if config.DROP_PREVIOUS_UPDATES:
        await bot.delete_webhook(drop_pending_updates=True)
    await setup_aiogram(dispatcher)
    dispatcher['aiogram_logger'].info('Started polling')


async def aiogram_on_shutdown_polling(dispatcher: Dispatcher, bot: Bot) -> None:
    dispatcher['aiogram_logger'].debug('Stopping polling')
    await bot.session.close()
    await dispatcher.storage.close()
    dispatcher['aiogram_logger'].info('Stopped polling')


# noinspection PyUnusedLocal
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    logger.info("Configuring Uvicorn")
    await bot.set_webhook(url=config.WEBHOOK_URL,
                          allowed_updates=dp.resolve_used_update_types(),
                          drop_pending_updates=True)
    await setup_aiogram(dp)
    logger.info(f"Webhook set: {config.WEBHOOK_URL}")
    yield
    await bot.delete_webhook()
    await bot.session.close()
    logger.info("Webhook deleted, bot session closed")


app = FastAPI(debug=False, lifespan=lifespan)
register_controllers(app)
get_webhook_settings().allow_cors_origins(app)


if config.USE_WEBHOOK:
    @app.post(config.WEBHOOK_PATH)
    async def bot_webhook(update: dict):
        telegram_update = types.Update(**update)
        await dp.feed_update(bot=bot, update=telegram_update)
        return status.HTTP_200_OK


def main() -> None:
    if config.USE_WEBHOOK:
        webhook_settings = get_webhook_settings()
        uvicorn.run(
            app,
            host=webhook_settings.host,
            port=webhook_settings.port,
            log_level="debug",
            access_log=True,
            reload=False,
        )
    else:
        dp.startup.register(aiogram_on_startup_polling)
        dp.shutdown.register(aiogram_on_shutdown_polling)
        asyncio.run(dp.start_polling(bot))


if __name__ == '__main__':
    main()
