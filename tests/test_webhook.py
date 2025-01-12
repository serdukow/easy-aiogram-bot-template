import os
import warnings

import structlog
import re
from environs import Env

logger = structlog.getLogger(__name__)

WEBHOOK_VARS = ["WEBHOOK_URL", "NGINX_HOST"]
env = Env()
env.read_env()


def test_webhook():
    """
    Check if WEBHOOK_URL and NGINX_HOST are set for Webhook.
    :return: AssertionError if WEBHOOK_URL or NGINX_HOST is not set or not valid.
    """
    if env.bool("USE_WEBHOOK", False):
        webhook_url = os.environ.get("WEBHOOK_URL")

        if webhook_url:
            if re.match(r"^https://[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", webhook_url):
                logger.info(f"Webhook is correctly configured: {webhook_url}.")
            else:
                logger.error(
                    f"WEBHOOK_URL is not in a valid format: {webhook_url}. "
                    f"It should be in the form of https://your-domain.com"
                )
                assert False, (
                    f"WEBHOOK_URL is not in a valid format: {webhook_url}. "
                    f"It should be in the form of https://your-domain.com"
                )
        else:
            logger.error("WEBHOOK_URL is missing. To set up the webhook, please add this variable.")
            assert False, "WEBHOOK_URL is missing. To set up the webhook, please add this variable."

        if "NGINX_HOST" in os.environ:
            logger.info("NGINX_HOST is configured.")
        else:
            logger.error("NGINX_HOST is missing. To set up Nginx, please add this variable.")
            assert False, "NGINX_HOST is missing. To set up Nginx, please add this variable."
    else:
        warnings.warn("Webhook is not configured. Please, set USE_WEBHOOK to true, then fill WEBHOOK_URL.")
