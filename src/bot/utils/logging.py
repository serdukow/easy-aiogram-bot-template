import logging
import sys
from logging.handlers import MemoryHandler

import structlog
from structlog.dev import ConsoleRenderer, KeyValueColumnFormatter, Column

from src.bot.core import config

YELLOW = '\033[93m'
MAGENTA = '\033[95m'
CYAN = '\033[96m'
GREEN = '\033[92m'
RED = '\033[91m'
RESET = '\033[0m'

cr = ConsoleRenderer(
    columns=[
        Column(
            'timestamp',
            KeyValueColumnFormatter(
                key_style=None,
                value_style=YELLOW,
                reset_style=RESET,
                value_repr=str,
            ),
        ),
        Column(
            'event',
            KeyValueColumnFormatter(
                key_style=None,
                value_style=MAGENTA,
                reset_style=RESET,
                value_repr=str,
            ),
        ),
        Column(
            '',
            KeyValueColumnFormatter(
                key_style=CYAN,
                value_style=GREEN,
                reset_style=RESET,
                value_repr=str,
            ),
        ),
    ]
)


def error_highlighter(logger, method_name, event_dict):
    if method_name == "error":
        event_dict["event"] = f"{RED}{event_dict['event']}{RESET}"
    return event_dict


def warning_highlighter(logger, method_name, event_dict):
    if method_name == "warning":
        event_dict["event"] = f"{YELLOW}{event_dict['event']}{RESET}"
    return event_dict


def setup_logger() -> structlog.typing.FilteringBoundLogger:
    logging.basicConfig(
        level=config.LOGGING_LEVEL,
        stream=sys.stdout,
    )

    log: structlog.typing.FilteringBoundLogger = structlog.get_logger(
        structlog.stdlib.BoundLogger,
    )

    shared_processors: list[structlog.typing.Processor] = [
        structlog.processors.add_log_level,
        error_highlighter,
        warning_highlighter
    ]

    processors: list[structlog.typing.Processor] = [*shared_processors]

    memory_handler = MemoryHandler(
        capacity=10,
        flushLevel=logging.ERROR,
        target=logging.FileHandler('bot.log')
    )
    memory_handler.setLevel(logging.ERROR)

    root_logger = logging.getLogger()
    root_logger.addHandler(memory_handler)

    processors.extend(
        [
            structlog.processors.TimeStamper(fmt='iso', utc=True),
            cr,
        ],
    )

    structlog.configure(
        processors=processors,
        wrapper_class=structlog.make_filtering_bound_logger(config.LOGGING_LEVEL),
    )

    return log
