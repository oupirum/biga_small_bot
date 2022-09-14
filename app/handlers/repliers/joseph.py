import json
import time
import random
import logging

import settings
from app import chats


_quotes_file_path = './data/joseph_quotes.json'
with open(_quotes_file_path, encoding='utf-8') as f:
    _quotes = json.loads(f.read())

_sessions = dict()


def reply(message, bot):
    chat_id = message.chat.id
    sender_name = message.from_user and message.from_user.username
    chat_name = message.chat.username or message.chat.title

    if not chats.is_active(str(chat_id)):
        return False

    if str(chat_id) not in _sessions:
        logging.info(f'Create session for chat {chat_name}')
        _sessions[str(chat_id)] = Session()
    session = _sessions.get(str(chat_id))

    time_passed_from_last = time.time() - session.last_reply_time
    if time_passed_from_last > settings.reply_joseph_session_min_interval:
        session.last_reply_time = time.time()
        session.length = 1

        quote = _get_quote(session.recent_messages)
        logging.info(
            f'Reply in chat {chat_name} after {round(time_passed_from_last / 60, 2)} min:\n'
            f'      {sender_name}> {message.text}\n'
            f'      {quote}'
        )
        bot.send_message(chat_id=chat_id, text=quote)

        return True

    if session.length < settings.reply_joseph_session_length:
        session.last_reply_time = time.time()
        session.length = session.length + 1

        quote = _get_quote(session.recent_messages)
        logging.info(
            f'Reply in chat {chat_name}:\n'
            f'      {sender_name}> {message.text}\n'
            f'      {quote}'
        )
        bot.send_message(chat_id=chat_id, text=quote)

        return True

    if session.length == settings.reply_joseph_session_length:
        logging.info(
            f'Reply in chat {chat_name}:\n'
            f'      {sender_name}> {message.text}'
        )

    return False


def _get_quote(recent_messages):
    while True:
        quotes = _quotes[:]
        random.shuffle(quotes)
        quote = random.choice(quotes)
        if quote not in recent_messages:
            recent_messages.add(quote)
            if len(recent_messages) > 10:
                recent_messages.pop()

            return quote


class Session:
    def __init__(self):
        self.last_reply_time = 0
        self.length = 0
        self.recent_messages = set()
