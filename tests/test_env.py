import os

import structlog

logger = structlog.getLogger(__name__)

REQUIRED_ENV_VARS = ["BOT_TOKEN", "MAINTENANCE_MODE"]

WEBHOOK_VARS = [
    "MAIN_WEBHOOK_ADDRESS",
    "WEBHOOK_SECRET_TOKEN",
    "WEBHOOK_LISTENING_HOST",
    "WEBHOOK_LISTENING_PORT",
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


def test_env_vars():
    """
    Check required envs.
    :return: AssertionError if not set.
    """
    missing_vars = [var for var in REQUIRED_ENV_VARS if var not in os.environ]

    if os.environ.get("USE_WEBHOOK", "False").lower() == "true":
        missing_vars.extend([var for var in WEBHOOK_VARS if var not in os.environ])

    if os.environ.get("USE_POSTGRES", "False").lower() == "true":
        missing_vars.extend([var for var in POSTGRES_VARS if var not in os.environ])

    if os.environ.get("USE_REDIS", "False").lower() == "true":
        missing_vars.extend([var for var in REDIS_VARS if var not in os.environ])

    assert not missing_vars, logger.error(f"Missing required envs: {', '.join(missing_vars)}")
