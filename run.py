import logging
import json

from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from environs import Env
from google.cloud import dialogflow


GOOGLE_APP_CREDS_ENV_VAR = 'GOOGLE_APPLICATION_CREDENTIALS'
BOT_TOKEN_ENV_VAR = 'BOT_TOKEN'


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

env = Env()
env.read_env()


def get_intent_text(project_id: str, session_id: str, text: str, language_code: str) -> str:
    """
    Returns the result of detect intent with texts as inputs.
    """
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    logger.info(f'Session {session_id} with language code {language_code}')

    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(request={'session': session, 'query_input': query_input})

    logger.info(f'Query text: {response.query_result.query_text}')
    logger.info(
        f'Detected intent: {response.query_result.intent.display_name} '
        f'(Confidence: {response.query_result.intent_detection_confidence})'
    )
    logger.info(f'Fulfillment text: {response.query_result.fulfillment_text}\n')

    return response.query_result.fulfillment_text


def get_google_creds() -> dict:
    """Get Google application credentials from the GOOGLE_APPLICATION_CREDENTIALS file."""
    with open(env(GOOGLE_APP_CREDS_ENV_VAR), 'r') as google_creds_file:
        return json.loads(google_creds_file.read())


def start_handler(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    update.message.reply_text('Здравствуйте')


def text_handler(update: Update, context: CallbackContext) -> None:
    """Send a message for an arbitrary text."""
    reply_text = get_intent_text(
            project_id=get_google_creds()['project_id'],
            session_id=update.effective_user.id,
            text=update.message.text,
            language_code=update.effective_user.language_code
        )
    update.message.reply_text(reply_text)


def main() -> None:
    bot_token = env(BOT_TOKEN_ENV_VAR)

    updater = Updater(bot_token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start_handler))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, text_handler, pass_user_data=True))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
