from typing import List
from google.cloud.firestore_v1 import DocumentSnapshot

from storage.firestore import db


def _get_collection():
    return db.collection('chats')


def add(chat):
    _get_collection() \
            .document(str(chat.id)) \
            .set({
                'id': str(chat.id),
                'name': chat.username or chat.title,
                'active': True,
            }, merge=True)


def update(chat_id: str, payload: dict):
    _get_collection().document(str(chat_id)).set(payload, merge=True)


def disable(chat_id: str):
    _get_collection().document(str(chat_id)).set({'active': False}, merge=True)


def get(chat_id: str) -> DocumentSnapshot:
    return _get_collection().document(str(chat_id)).get()


def get_active_list() -> List[DocumentSnapshot]:
    return _get_collection().where('active', '==', True).get()


def is_active(chat_id: str):
    query = _get_collection().where('id', '==', str(chat_id)).where('active', '==', True)
    return len(query.get()) == 1
