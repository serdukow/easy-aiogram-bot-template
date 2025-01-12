import os
import re
import structlog
import warnings
from environs import Env

logger = structlog.getLogger(__name__)

REQUIRED_ENV_VARS = ["BOT_TOKEN"]
POSTGRES_VARS = ["PG_HOST", "PG_PORT", "PG_USER", "PG_PSSWRD", "PG_NAME"]

env = Env()
env.read_env()


def test_polling():
    """
    Check if bot is ready for polling with valid BOT_TOKEN format.
    :return: AssertionError if BOT_TOKEN is not set or has invalid format.
    """
    missing_vars = []

    bot_token = os.environ.get("BOT_TOKEN")
    if not bot_token:
        logger.error("BOT_TOKEN is missing. Bot cannot run.")
        missing_vars.append("BOT_TOKEN")
    else:
        if not re.match(r"^\d+:[a-zA-Z0-9_-]+$", bot_token):
            logger.error(f"Bot token is invalid: {bot_token}")
            missing_vars.append("BOT_TOKEN")
        else:
            logger.info("BOT_TOKEN is set. Bot is ready for polling.")

    if os.environ.get("USE_POSTGRES", "False").lower() == "true":
        for var in POSTGRES_VARS:
            if not os.environ.get(var):
                logger.warning(f"Postgres variable {var} is missing. Please configure it.")
                missing_vars.append(var)
    else:
        warnings.warn("Postgres is not set. This may lead to issues when working with the database. "
                      "Please ensure that you have configured your database, then set USE_POSTGRES to true "
                      f"and fill other connection properties {POSTGRES_VARS}")

    if missing_vars:
        assert False, f"Missing required environment variables: {', '.join(missing_vars)}"
