from typing import Tuple

import settings
from app import chats


JokeType = {
    'Joke': 11,
    'Story': 12,
    'Rhyme': 13,
    'Aphorism': 14,
    'Quote': 15,
    'Toast': 16,
    'Status': 18,
}


def get_types(chat_id: str):
    chat = chats.get(chat_id)
    if chat.exists:
        data = chat.to_dict()
        return data.get('joke_types', settings.default_joke_types)
    return settings.default_joke_types


def update_types(chat_id: str, type_ids: Tuple[int]):
    chats.update(chat_id, {'joke_types': type_ids})


def get_timer(chat_id: str):
    chat = chats.get(chat_id)
    if chat.exists:
        data = chat.to_dict()
        return (
            data.get('last_joke_time'),
            data.get('joker_interval', settings.default_joker_interval)
        )
    return None, settings.default_joker_interval


def update_last_joke_time(chat_id: str, timestamp: int):
    chats.update(chat_id, {'last_joke_time': timestamp})


def update_interval(chat_id: str, seconds: int):
    chats.update(chat_id, {'joker_interval': seconds})


def get_sleep_interval(chat_id: str):
    chat = chats.get(chat_id)
    if chat.exists:
        data = chat.to_dict()
        return (
            data.get('joker_sleep_from', settings.default_joker_sleep_from),
            data.get('joker_sleep_to', settings.default_joker_sleep_to)
        )
    return settings.default_joker_sleep_from, settings.default_joker_sleep_to


def update_sleep_interval(chat_id: str, from_hour: int, to_hour: int):
    chats.update(chat_id, {
        'joker_sleep_from': from_hour,
        'joker_sleep_to': to_hour,
    })
