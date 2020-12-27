Chat bot with a simple intent classification.

## Set up:
Set environment variables:
* TELEGRAM_BOT_TOKEN - Telegram bot token. Can be obtained from [Bot Father](https://telegram.me/BotFather).
* VK_BOT_TOKEN - Vkontakte.ru bot token. Generated at the VK group administration panel.
* GOOGLE_APPLICATION_CREDENTIALS - Path to a [GOOGLE_APPLICATION_CREDENTIALS file](https://cloud.google.com/docs/authentication/getting-started).

## Usage:
* Run Telegram bot.
    > python run.py telegram_bot

* Run VK bot.
    > python run.py vk_bot

* Train the bot with provided phrases. For the format information, check the [example](https://github.com/aevtikheev/dvmn_support_bot/blob/master/intents.json).
    > python run.py train -f intents.json
