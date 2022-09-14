from telegram.ext import CommandHandler, Filters, MessageHandler, CallbackQueryHandler
import logging

import settings
from app import api, chats

from app.commands.start import start_handler
from app.commands.stop import stop_handler
from app.commands.restart import create_restart_handler
from app.commands.help import help_handler
from app.commands.set_jokes import set_joke_types_handler, set_joke_interval_handler,\
    set_joke_sleep_time_handler
from app.handlers.callback_query import callback_query_handler

from app.handlers.joined_chat import joined_chat_handler
from app.handlers.left_chat import left_chat_handler
from app.handlers.message import message_handler
from app.handlers.photo import photo_handler
from app.handlers.video import video_handler

from app.modules.joker.joker_service import JokerService


def main():
    logging.basicConfig(
        format='%(asctime)s - %(filename)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

    setup_services()

    updater = api.create_updater()
    setup_handlers(updater)

    updater.start_polling()
    updater.idle()


def setup_handlers(updater):
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start_handler))
    dispatcher.add_handler(CommandHandler(settings.stop_word, stop_handler))
    dispatcher.add_handler(CommandHandler('restart', create_restart_handler(updater)))
    dispatcher.add_handler(CommandHandler('help', help_handler))
    dispatcher.add_handler(CommandHandler('set_joke_types', set_joke_types_handler))
    dispatcher.add_handler(CommandHandler('set_joke_interval', set_joke_interval_handler))
    dispatcher.add_handler(CommandHandler('set_joke_sleep_time', set_joke_sleep_time_handler))

    dispatcher.add_handler(MessageHandler(Filters.status_update.new_chat_members, joined_chat_handler))
    dispatcher.add_handler(MessageHandler(Filters.status_update.left_chat_member, left_chat_handler))

    dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), message_handler))
    dispatcher.add_handler(MessageHandler(Filters.photo, photo_handler))
    dispatcher.add_handler(MessageHandler(Filters.video, video_handler))

    dispatcher.add_handler(CallbackQueryHandler(callback_query_handler))

    logging.info('Listening for events')


def setup_services():
    JokerService().start()


if __name__ == '__main__':
    main()
