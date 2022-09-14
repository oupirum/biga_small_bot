from telegram import Update

import settings
from app import admin_menu
from app.handlers.repliers import joseph
from app.modules.broadcaster import broadcaster


_repliers = [
    joseph.reply,
]


def message_handler(update: Update, context):
    if update.effective_chat and update.effective_chat.type == 'private' and update.effective_chat.username in settings.admins:
        chat_id = str(update.effective_chat.id)
        if broadcaster.is_started(chat_id):
            text = update.effective_message.text_html_urled

            broadcaster.add_message(chat_id, text)

            admin_menu.show_broadcast_options(chat_id, context.bot)

            return

    if update.effective_message and update.effective_message.chat:
        for reply in _repliers:
            replied = reply(update.effective_message, context.bot)
            if replied:
                break
