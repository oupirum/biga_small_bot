import logging

from app import chats


def joined_chat_handler(update, context):
    for member in update.effective_message.new_chat_members:
        if member.username == context.bot.username:
            chats.add(update.effective_chat)

            chat_id = update.effective_chat.id
            chat_name = update.effective_chat.username or update.effective_chat.title
            logging.info(f'Added to chat {chat_id}: {chat_name}')
