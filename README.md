Support bot with a simple intent classification via Dialogflow. Works with [VK](https://vk.com)
and [Telegram](https://telegram.org/). Also supports error reporting to a Telegram chat.

![example](https://github.com/aevtikheev/dvmn_support_bot/blob/master/docs/images/tg_bot.gif)

## Set up:
Set environment variables:
* TELEGRAM_BOT_TOKEN - Telegram bot token. Can be obtained from [Bot Father](https://telegram.me/BotFather).
* VK_BOT_TOKEN - Vkontakte.ru bot token. Generated at the VK group administration panel.
* GOOGLE_APPLICATION_CREDENTIALS - Path to a [GOOGLE_APPLICATION_CREDENTIALS file](https://cloud.google.com/docs/authentication/getting-started).
* TELEGRAM_REPORT_BOT_TOKEN - Telegram bot token for the error reporting bot.
* TELEGRAM_REPORT_CHAT_ID - ID of a telegram chat for error reporting. [How to get](https://stackoverflow.com/questions/32423837/telegram-bot-how-to-get-a-group-chat-id).
* VK_LANGUAGE_CODE - Dialogflow Intent language code which will be used to handle VK messages.

## Usage:
* Run Telegram bot.
    > python run.py telegram_bot

* Run VK bot.
    > python run.py vk_bot

* Train the bot with provided phrases. For the format information, check the [example](https://github.com/aevtikheev/dvmn_support_bot/blob/master/intents.json).
    > python run.py train -f intents.json

## Demo
 * Telegram version of a bot lives here - @ae_dvmn_support_bot
 * VK version - https://vk.com/club201440450