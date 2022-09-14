from telegram import Update
import logging

import settings
from app import chats, admin_menu


def start_handler(update: Update, context):
    chats.add(update.effective_chat)

    chat_id = update.effective_chat.id
    chat_name = update.effective_chat.username or update.effective_chat.title
    logging.info(f'Started in chat {chat_id}: {chat_name}')

    if update.effective_chat.type == 'private' and update.effective_chat.username in settings.admins:
        admin_menu.show_menu(str(chat_id), context.bot)

        return

    text = 'Привет, извращенец!' if update.effective_chat.type == 'private' else 'Привет, извращенцы!'
    context.bot.send_message(chat_id=chat_id, text=text)

