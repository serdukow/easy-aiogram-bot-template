import os
import structlog
from environs import Env

logger = structlog.getLogger(__name__)

REQUIRED_ENV_VARS = ["BOT_TOKEN", "MAINTENANCE_MODE"]

WEBHOOK_VARS = [
    "WEBHOOK_URL"
]

POSTGRES_VARS = [
    "PG_HOST",
    "PG_PORT",
    "PG_USER",
    "PG_PSSWRD",
    "PG_NAME",
]

REDIS_VARS = [
    "REDIS_HOST",
    "REDIS_PORT",
    "REDIS_PSSWRD",
]

env = Env()
env.read_env()


def test_env_vars():
    """
    Check required envs.
    :return: AssertionError if not set.
    """
    missing_vars = [var for var in REQUIRED_ENV_VARS if var not in os.environ]

    if env.bool("USE_WEBHOOK", False):
        missing_vars.extend([var for var in WEBHOOK_VARS if var not in os.environ])

    if env.bool("USE_POSTGRES", False):
        missing_vars.extend([var for var in POSTGRES_VARS if var not in os.environ])

    if env.bool("USE_REDIS", False):
        missing_vars.extend([var for var in REDIS_VARS if var not in os.environ])

    assert not missing_vars, logger.error(f"Missing required envs: {', '.join(missing_vars)}")