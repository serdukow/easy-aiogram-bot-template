import structlog

from .base import BaseOrm
from .user import UserOrm

logger = structlog.get_logger(__name__)


async def async_create_tables(async_engine):
    try:
        async with async_engine.begin() as conn:
            await conn.run_sync(BaseOrm.metadata.create_all)
            logger.info('Tables created successfully 🐘')
    except Exception as e:
        logger.error(f'Error connecting to postgres or creating tables 🐘', detail=str(e))
