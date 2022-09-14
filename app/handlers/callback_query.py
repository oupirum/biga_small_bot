import logging

import settings
from app import admin_menu
from app.modules.broadcaster import broadcaster


def callback_query_handler(update, context):
    logging.info(f'Handle query from {update.effective_chat.username}')
    if update.effective_chat.type == 'private' and update.effective_chat.username in settings.admins:
        admin_chat_id = update.effective_chat.id
        query = update.callback_query
        logging.info(f'Query: {query.data}')

        if query.data == 'init_broadcast':
            broadcaster.start(str(admin_chat_id))

            text = 'Теперь отправь сюда текст/фотографии, чтобы я разослал их в группы'
            context.bot.send_message(chat_id=admin_chat_id, text=text)

        if query.data.startswith('send_to_chat_') and broadcaster.has_data(str(admin_chat_id)):
            target_chat_id = query.data.replace('send_to_chat_', '')
            broadcaster.send_to_chat(target_chat_id, str(admin_chat_id), context.bot)

            context.bot.send_message(chat_id=admin_chat_id, text='Отправлено')
            admin_menu.show_broadcast_options(str(admin_chat_id), context.bot)

        if query.data == 'broadcast' and broadcaster.has_data(str(admin_chat_id)):
            broadcaster.broadcast(str(admin_chat_id), context.bot)

            context.bot.send_message(chat_id=admin_chat_id, text='Отправлено')
            admin_menu.show_menu(str(admin_chat_id), context.bot)
            broadcaster.reset(str(admin_chat_id))

        if query.data == 'cancel_broadcast':
            broadcaster.reset(str(admin_chat_id))

            admin_menu.show_menu(str(admin_chat_id), context.bot)

        query.answer()
