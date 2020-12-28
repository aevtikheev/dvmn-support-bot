"""Module to work with environment variables. """
from dataclasses import dataclass

from environs import Env


@dataclass
class EnvSettings:
    """Environment settings for Support Bot."""
    tg_bot_token: str
    vk_bot_token: str
    google_app_creds_file: str
    tg_report_bot_token: str
    tg_report_chat_id: str
    vk_language_code: str


def get_env_settings() -> EnvSettings:
    """Read environment settings."""
    env = Env()
    env.read_env()
    return EnvSettings(
        tg_bot_token=env('TELEGRAM_BOT_TOKEN', None),
        vk_bot_token=env('VK_BOT_TOKEN', None),
        google_app_creds_file=env('GOOGLE_APPLICATION_CREDENTIALS', None),
        tg_report_bot_token=env('TELEGRAM_REPORT_BOT_TOKEN', None),
        tg_report_chat_id=env('TELEGRAM_REPORT_CHAT_ID', None),
        vk_language_code=env('VK_LANGUAGE_CODE', None)
    )


env_settings = get_env_settings()
