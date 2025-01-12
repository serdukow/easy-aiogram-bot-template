import os
import structlog
from environs import Env

logger = structlog.getLogger(__name__)

WEBHOOK_VARS = ["WEBHOOK_URL", "NGINX_HOST"]
env = Env()
env.read_env()


def test_webhook():
    """
    Check if WEBHOOK_URL and NGINX_HOST are set for Webhook.
    :return: AssertionError if WEBHOOK_URL or NGINX_HOST is not set.
    """
    if env.bool("USE_WEBHOOK", False):
        if "WEBHOOK_URL" in os.environ:
            logger.info("Webhook is configured with WEBHOOK_URL.")
        else:
            logger.error("WEBHOOK_URL is missing. To set up the webhook, please add this variable.")
            assert False, "WEBHOOK_URL is missing. To set up the webhook, please add this variable."

        if "NGINX_HOST" in os.environ:
            logger.info("NGINX_HOST is configured.")
        else:
            logger.error("NGINX_HOST is missing. To set up Nginx, please add this variable.")
            assert False, "NGINX_HOST is missing. To set up Nginx, please add this variable."
