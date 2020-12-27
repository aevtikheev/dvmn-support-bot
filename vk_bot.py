"""VK version of a support bot."""
import logging
import random

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from environs import Env

import dialogflow


BOT_TOKEN_ENV_VAR = 'VK_BOT_TOKEN'
LANGUAGE_CODE = 'EN'  # Language code passed to Dialogflow API


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

env = Env()
env.read_env()


def reply_from_dialogflow(event, api):
    response = dialogflow.get_response(
            session_id=event.user_id,
            text=event.message,
            language_code=LANGUAGE_CODE
        )
    if not response.is_fallback:
        api.messages.send(
            user_id=event.user_id,
            message=response.text,
            random_id=random.randint(-2147483648, 2147483647)  # random_id must be a random INT32
        )


def run() -> None:
    """Run VK bot."""
    session = vk_api.VkApi(token=env(BOT_TOKEN_ENV_VAR))
    api = session.get_api()
    longpoll = VkLongPoll(session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            reply_from_dialogflow(event, api)
