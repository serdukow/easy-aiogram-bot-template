import os
import structlog
from environs import Env

logger = structlog.getLogger(__name__)

REQUIRED_ENV_VARS = ["BOT_TOKEN", "MAINTENANCE_MODE"]

env = Env()
env.read_env()


def test_polling():
    """
    Check if BOT_TOKEN is set for Polling.
    :return: AssertionError if BOT_TOKEN is not set.
    """
    if "BOT_TOKEN" in os.environ:
        logger.info("Bot is ready for polling.")
    else:
        logger.error("BOT_TOKEN is missing. Bot cannot run.")
        assert False, "BOT_TOKEN is missing. Bot cannot run."
