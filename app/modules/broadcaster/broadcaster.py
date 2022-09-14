import logging
import time
from typing import List

import telegram
from google.cloud.firestore_v1 import DocumentSnapshot
from telegram import InputMediaPhoto, InputMediaVideo

from app import chats
from storage.firestore import db


def _get_collection():
    return db.collection('broadcast')


def start(admin_chat_id: str):
    logging.info(f'Start broadcaster in {admin_chat_id}')
    reset(admin_chat_id)
    _get_collection() \
            .document(admin_chat_id) \
            .set({
                'id': admin_chat_id,
            })


def is_started(admin_chat_id: str):
    return _get_collection() \
            .document(admin_chat_id) \
            .get() \
            .exists


def add_photo(admin_chat_id: str, file_id: str, media_group_id: str, caption: str):
    logging.info(f'Add photo {file_id} {f"in media group {media_group_id}" if media_group_id else ""}')
    _get_collection() \
            .document(admin_chat_id) \
            .collection('data') \
            .add({
                'type': 'photo',
                'file_id': file_id,
                'caption': caption,
                'media_group_id': media_group_id,
                'timestamp': time.time(),
            })


def add_video(admin_chat_id: str, file_id: str, media_group_id: str, caption: str):
    logging.info(f'Add video {file_id} {f"in media group {media_group_id}" if media_group_id else ""}')
    _get_collection() \
            .document(admin_chat_id) \
            .collection('data') \
            .add({
                'type': 'video',
                'file_id': file_id,
                'caption': caption,
                'media_group_id': media_group_id,
                'timestamp': time.time(),
            })


def add_message(admin_chat_id: str, text: str):
    logging.info(f'Add message {text}')
    _get_collection() \
            .document(admin_chat_id) \
            .collection('data') \
            .add({
                'type': 'text',
                'text': text,
                'timestamp': time.time(),
            })


def set_menu_id(admin_chat_id: str, menu_id: int):
    logging.info(f'Set menu id {admin_chat_id} {menu_id}')
    _get_collection() \
            .document(admin_chat_id) \
            .set({
                'menu_id': menu_id,
            }, merge=True)


def get_menu_id(admin_chat_id: str):
    return _get_collection() \
            .document(admin_chat_id) \
            .get() \
            .to_dict() \
            .get('menu_id')


def send_to_chat(target_chat_id: str, admin_chat_id: str, bot):
    entities = _get_typed_entities(admin_chat_id)
    _send_to_chat(target_chat_id, entities, bot)


def broadcast(admin_chat_id: str, bot):
    entities = _get_typed_entities(admin_chat_id)
    chat_ids = [str(chat.id) for chat in chats.get_active_list()]
    logging.info(f'Broadcast {len(entities)} entities for {len(chat_ids)} chats')

    for target_chat_id in chat_ids:
        try:
            _send_to_chat(target_chat_id, entities, bot)
        except:
            logging.exception('Broadcast error')


def _send_to_chat(target_chat_id: str, entities: list, bot):
    logging.info(f'Send {len(entities)} entities to {target_chat_id}')
    for entity in entities:
        if entity.type == 'mediagroup':
            bot.send_media_group(target_chat_id, entity.value)
        else:
            bot.send_message(target_chat_id, entity.value, parse_mode=telegram.ParseMode.HTML)


def reset(admin_chat_id: str):
    logging.info(f'Reset {admin_chat_id}')
    for entity in get_data(admin_chat_id):
        entity.reference.delete()

    _get_collection() \
            .document(admin_chat_id) \
            .delete()


def has_data(admin_chat_id: str):
    return len(get_data(admin_chat_id)) > 0


def get_data(admin_chat_id: str) -> List[DocumentSnapshot]:
    return _get_collection() \
            .document(admin_chat_id) \
            .collection('data') \
            .order_by('timestamp') \
            .get()


def get_media(admin_chat_id: str) -> List[DocumentSnapshot]:
    data = get_data(admin_chat_id)
    return list(filter(lambda entity: entity.get('type') in ['photo', 'video'], data))


def _get_typed_entities(admin_chat_id):
    data = get_data(admin_chat_id)
    typed_items = []
    for item in data:
        if item.get('type') == 'photo':
            photo = InputMediaPhoto(
                item.get('file_id'),
                caption=item.get('caption') if item.get('caption') else None
            )
            if len(typed_items) == 0 or typed_items[-1].type != 'mediagroup':
                typed_items.append(DataEntity('mediagroup', []))
            typed_items[-1].value.append(photo)

        if item.get('type') == 'video':
            video = InputMediaVideo(
                item.get('file_id'),
                caption=item.get('caption') if item.get('caption') else None
            )
            if len(typed_items) == 0 or typed_items[-1].type != 'mediagroup':
                typed_items.append(DataEntity('mediagroup', []))
            typed_items[-1].value.append(video)

        if item.get('type') == 'text':
            typed_items.append(DataEntity('text', item.get('text')))

    return typed_items


class DataEntity:
    def __init__(self, type, value):
        self.type = type
        self.value = value
