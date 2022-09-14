from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from app import chats
from app.modules.broadcaster import broadcaster


def show_menu(admin_chat_id: str, bot):
    text = 'Опции:'
    keyboard = [
        [InlineKeyboardButton('Сделать рассылку', callback_data='init_broadcast')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    bot.send_message(chat_id=admin_chat_id, text=text, reply_markup=reply_markup)


def show_broadcast_options(admin_chat_id: str, bot, update=False):
    files = broadcaster.get_data(admin_chat_id)
    text = f'Получено объектов: {len(files)}\nОтправить в:'

    keyboard = []
    for chat in chats.get_active_list():
        if chat.get('id') == admin_chat_id:
            continue
        keyboard.append([InlineKeyboardButton(f'👥 {chat.get("name")}', callback_data=f'send_to_chat_{chat.get("id")}')])

    keyboard.append([InlineKeyboardButton('📢 Во все перечисленные', callback_data='broadcast')])
    keyboard.append([InlineKeyboardButton('✖️ Отмена', callback_data='cancel_broadcast')])
    reply_markup = InlineKeyboardMarkup(keyboard)

    menu_id = broadcaster.get_menu_id(admin_chat_id)
    if update and menu_id:
        bot.edit_message_text(
            chat_id=admin_chat_id,
            message_id=menu_id,
            text=text,
            reply_markup=reply_markup,
        )
    else:
        message = bot.send_message(
            chat_id=admin_chat_id,
            text=text,
            reply_markup=reply_markup,
        )

        broadcaster.set_menu_id(admin_chat_id, message.message_id)
