from telegram import Update

import settings
from app import admin_menu
from app.modules.broadcaster import broadcaster


def photo_handler(update: Update, context):
    if update.effective_chat and update.effective_chat.type == 'private' and \
            update.effective_chat.username in settings.admins:
        chat_id = str(update.effective_chat.id)
        if broadcaster.is_started(chat_id):
            file_id = update.effective_message.photo[0].file_id
            caption = update.effective_message.caption
            media_group_id = update.effective_message.media_group_id

            broadcaster.add_photo(chat_id, file_id, media_group_id, caption)

            should_update = False
            if media_group_id:
                files = broadcaster.get_media(chat_id)
                files_in_media_group = list(filter(lambda file: file.get('media_group_id') == media_group_id, files))
                should_update = len(files_in_media_group) > 1

            admin_menu.show_broadcast_options(chat_id, context.bot, update=should_update)
