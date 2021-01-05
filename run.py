"""Entry point to operate with a support bot."""
import logging
import logging.config
import argparse
import sys
import json

import telegram_bot
import vk_bot
import dialogflow
from logger import LOGGING_CONFIG


CMD_TELEGRAM_BOT = 'telegram_bot'
CMD_TRAIN_DIALOGFLOW = 'train'
CMD_VK_BOT = 'vk_bot'


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command')

    subparsers.add_parser(CMD_TELEGRAM_BOT, help='Run telegram bot')
    subparsers.add_parser(CMD_VK_BOT, help='Run VK bot')

    parser_train_dialogflow = subparsers.add_parser(
        CMD_TRAIN_DIALOGFLOW,
        help='Train Dialogflow with provided intents'
    )
    parser_train_dialogflow.add_argument(
        '-f', '--file', type=argparse.FileType('r'),
        help='Path to a file with intents',
        required=True
    )

    if len(sys.argv) <= 1:
        sys.argv.append('--help')

    return parser.parse_args()


def main() -> None:
    logging.config.dictConfig(LOGGING_CONFIG)

    args = parse_args()
    if args.command == CMD_TELEGRAM_BOT:
        telegram_bot.start_bot()
    elif args.command == CMD_VK_BOT:
        vk_bot.start_bot()
    elif args.command == CMD_TRAIN_DIALOGFLOW:
        with args.file as file:
            intents = json.loads(file.read())
        dialogflow.train_agent(intents)


if __name__ == '__main__':
    main()
