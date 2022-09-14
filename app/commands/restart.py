import os
import sys
from threading import Thread
import logging

import settings


def create_restart_handler(updater):
    def stop_and_restart():
        updater.stop()
        os.execl(sys.executable, sys.executable, *sys.argv)

    def restart_handler(update, context):
        if update.effective_message.from_user.username in settings.admins:
            update.effective_message.reply_text('Bot is restarting...')
            logging.info('Restarting...')
            Thread(target=stop_and_restart).start()

    return restart_handler
