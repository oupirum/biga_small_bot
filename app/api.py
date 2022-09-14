from telegram import Bot
from telegram.ext import Updater

import settings


def create_updater():
    return Updater(token=settings.api_token)


def create_bot():
    return Bot(token=settings.api_token)
