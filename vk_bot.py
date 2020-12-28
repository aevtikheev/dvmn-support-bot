"""VK version of a support bot."""
import logging
import random

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType, Event
from vk_api.vk_api import VkApiMethod

import dialogflow
from logger import TelegramLogsHandler, exception_logger
from env_settings import env_settings


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__file__)
logger.addHandler(TelegramLogsHandler())


def reply_from_dialogflow(event: Event, api: VkApiMethod) -> None:
    """Send answer for a detected intent. Do nothing if intent was not detected."""
    response = dialogflow.get_response(
            session_id=event.user_id,
            text=event.message,
            language_code=env_settings.vk_language_code
        )
    if not response.is_fallback:
        api.messages.send(
            user_id=event.user_id,
            message=response.text,
            random_id=random.randint(-2147483648, 2147483647)  # random_id must be a random INT32
        )


def run() -> None:
    """Run VK bot."""
    session = vk_api.VkApi(token=env_settings.vk_bot_token)
    api = session.get_api()
    longpoll = VkLongPoll(session)

    with exception_logger(Exception, logger, raise_=True):
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                reply_from_dialogflow(event, api)
