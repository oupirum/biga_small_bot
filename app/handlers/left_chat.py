import logging

from app import chats


def left_chat_handler(update, context):
    if update.effective_message.left_chat_member.username == context.bot.username:
        chat_id = update.effective_chat.id
        chat_name = update.effective_chat.username or update.effective_chat.title

        chats.disable(str(chat_id))

        logging.info(f'Removed from chat {chat_id}: {chat_name}')
