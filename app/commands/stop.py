from telegram import Update
import logging

from app import chats


def stop_handler(update: Update, context):
    chat_id = update.effective_chat.id
    chats.disable(chat_id)

    context.bot.send_message(
        chat_id=chat_id,
        text='Хорошо, хорошо. Замолкаю 😗',
    )

    chat_name = update.effective_chat.username or update.effective_chat.title
    logging.info(f'Stopped in chat {chat_id}: {chat_name}')
