"""Common code related to logging."""
import logging
from contextlib import contextmanager
from typing import Union, Tuple, Type

import telegram

from env_settings import env_settings


LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] [%(pathname)s:%(lineno)d] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
        },
        'telegram': {  # Logs output to a specified telegram chat.
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'telegram_logger.TelegramLogsHandler',
        },
    },
    'loggers': {
        '': {
            'handlers': ['default'],
            'level': 'INFO',
        },
        'telegram': {  # Logger for a Telegram bot that sends output to the telegram chat
            'handlers': ['telegram'],
            'level': 'INFO',
        },
        'vk': {  # Logger for a VK bot that sends output to the telegram chat
            'handlers': ['telegram'],
            'level': 'INFO',
        }
    }
}


class TelegramLogsHandler(logging.Handler):
    """Log handler which sends logs to a specified telegram chat."""
    def __init__(self):
        self._bot = telegram.Bot(token=env_settings.tg_report_bot_token)
        self._chat_id = env_settings.tg_report_chat_id
        super().__init__()

    def emit(self, record):
        log_entry = self.format(record)
        self._bot.send_message(chat_id=self._chat_id, text=log_entry)


@contextmanager
def exception_logger(
        exceptions: Union[Type[Exception], Tuple[Type[Exception]]],
        logger: logging.Logger,
        raise_: bool = True
) -> None:
    """
    Context manager that catches specified exceptions and logs them with a provided logger.

    :param exceptions: Exceptions to catch.
    :param logger: Logger which will log caught exceptions.
    :param raise_: Flag to raise caught exception or not.
    """
    try:
        yield
    except exceptions as exception:
        logger.exception(exception)
        if raise_:
            raise
