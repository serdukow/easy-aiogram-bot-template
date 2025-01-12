from typing import Union

from environs import Env


env = Env()
env.read_env()

MAINTENANCE_MODE: bool = env.bool("MAINTENANCE_MODE", False)

BOT_TOKEN: str = env.str("BOT_TOKEN")
BOT_ID: str = BOT_TOKEN.split(":")[0]
BOT_API: str = BOT_TOKEN.split(":")[1]
GROUP_ID: int = env.int("GROUP_ID", None)
ADMINS_IDS: Union[int, list[int]] = env.list("ADMIN_IDS", subcast=int)

USE_POSTGRES: str = env.str("USE_POSTGRES", False)
if USE_POSTGRES:
    PG_HOST: str = env.str("PG_HOST")
    PG_PORT: int = env.int("PG_PORT", 5432)
    PG_USER: str = env.str("PG_USER")
    PG_PSSWRD: str = env.str("PG_PSSWRD")
    PG_NAME: str = env.str("PG_NAME")

USE_REDIS: bool = env.bool("USE_REDIS", False)
if USE_REDIS:
    REDIS_HOST: str = env.str("REDIS_HOST")
    REDIS_PORT: int = env.int("REDIS_PORT", 6379)
    REDIS_PSSWRD: str = env.str("REDIS_PSSWRD")

USE_WEBHOOK: bool = env.bool("USE_WEBHOOK", False)
if USE_WEBHOOK:
    WEBHOOK_PATH: str = f"/webhook/{BOT_ID}"

    WEBHOOK_HOST: str = env.str("WEBHOOK_HOST")
    WEBHOOK_URL = WEBHOOK_HOST + WEBHOOK_PATH

    WEBHOOK_SECRET_TOKEN: str = env.str("WEBHOOK_SECRET_TOKEN")
    WEBHOOK_LISTENING_HOST: str = env.str("WEBHOOK_LISTENING_HOST", "localhost")
    WEBHOOK_LISTENING_PORT: int = env.int("WEBHOOK_LISTENING_PORT", 3000)

    MAX_UPDATES_IN_QUEUE: int = env.int("MAX_UPDATES_IN_QUEUE", 100)

USE_NGINX: bool = env.bool("NGINX_HOST", False)
if USE_NGINX:
    NGINX_HOST: str = env.str("NGINX_HOST")

LOGGING_LEVEL: int = env.int("LOGGING_LEVEL", 10)
DROP_PREVIOUS_UPDATES: bool = env.bool("DROP_PREVIOUS_UPDATES", False)
