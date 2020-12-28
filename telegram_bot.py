"""Telegram version of a support bot."""

import logging

from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from env_settings import env_settings

import dialogflow
from logger import TelegramLogsHandler, exception_logger


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__file__)
logger.addHandler(TelegramLogsHandler())


def _start_handler(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    update.message.reply_text('Здравствуйте')


def _text_handler(update: Update, context: CallbackContext) -> None:
    """Send a message for an arbitrary text."""
    response = dialogflow.get_response(
            session_id=update.effective_user.id,
            text=update.message.text,
            language_code=update.effective_user.language_code
        )
    update.message.reply_text(response.text)


def run() -> None:
    """Run Telegram bot."""
    bot_token = env_settings.tg_bot_token
    updater = Updater(bot_token)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", _start_handler))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, _text_handler, pass_user_data=True))

    with exception_logger(Exception, logger, raise_=True):
        updater.start_polling()
        updater.idle()
