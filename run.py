"""Entry point to operate with a support bot."""

import argparse
import sys
import json

import telegram_bot
import dialogflow


CMD_TELEGRAM_BOT = 'telegram_bot'
CMD_TRAIN_DIALOGFLOW = 'train_dialogflow'


def parse_args():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command')

    subparsers.add_parser(CMD_TELEGRAM_BOT, help='Run telegram bot')

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


def main():
    args = parse_args()
    if args.command == CMD_TELEGRAM_BOT:
        telegram_bot.run()
    elif args.command == CMD_TRAIN_DIALOGFLOW:
        with args.file as file:
            intents = json.loads(file.read())
        dialogflow.train(intents)


if __name__ == '__main__':
    main()
