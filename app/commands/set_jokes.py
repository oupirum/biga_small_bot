from telegram import Update
import logging

import settings
from app.modules.joker import joker_settings


def set_joke_types_handler(update: Update, context):
    if not update.effective_message or not update.effective_message.text:
        return

    message = update.effective_message
    chat_id = message.chat.id
    if _is_from_admin(message, context.bot):
        command, argument = f'{message.text} '.split(' ', 2)[0:2]
        logging.info(f'Set joke types: {argument}')
        if argument:
            type_names = [
                    type_name.strip()
                    for type_name in argument.split(',')
                    if type_name.strip() in joker_settings.JokeType]
            type_ids = [
                    joker_settings.JokeType[type_name.strip()]
                    for type_name in type_names]
        else:
            type_ids = settings.default_joke_types
            type_names = [
                    type_name
                    for type_name, type_id in joker_settings.JokeType.items()
                    if type_id in type_ids]

        if len(type_ids) > 0:
            joker_settings.update_types(str(chat_id), tuple(type_ids))

            logging.info(f'Set joke types: {type_names} for chat {chat_id}')
            context.bot.send_message(chat_id, f'Типы изменены: {", ".join(type_names)}')
    else:
        context.bot.send_message(chat_id, 'Разрешено только админам')


def set_joke_interval_handler(update: Update, context):
    if not update.effective_message or not update.effective_message.text:
        return

    message = update.effective_message
    chat_id = message.chat.id
    if _is_from_admin(message, context.bot):
        command, argument = f'{message.text} '.split(' ', 2)[0:2]
        logging.info(f'Set joke interval: {argument}')
        if argument:
            hours = float(argument.strip())
            seconds = int(60 * 60 * hours)
        else:
            seconds = settings.default_joker_interval
            hours = seconds / 60 / 60

        if 60 * 10 < seconds < 60 * 60 * 24 * 7:
            joker_settings.update_interval(chat_id, seconds)
            context.bot.send_message(
                chat_id,
                f'Интервал изменен: {round(hours) if hours % 1 == 0 else hours} часа(ов)',
            )
        else:
            context.bot.send_message(
                chat_id,
                'Интервал должен быть не меньше 10 минут и не больше 7 дней',
            )
    else:
        context.bot.send_message(chat_id, 'Разрешено только админам')


def set_joke_sleep_time_handler(update: Update, context):
    if not update.effective_message or not update.effective_message.text:
        return

    message = update.effective_message
    chat_id = message.chat.id
    if _is_from_admin(message, context.bot):
        command, from_hour, to_hour,  = f'{message.text}  '.split(' ', 3)[0:3]
        logging.info(f'Set joke sleep: {from_hour} {to_hour}')
        if from_hour and to_hour:
            from_hour = int(from_hour.strip())
            to_hour = int(to_hour.strip())
        else:
            from_hour = settings.default_joker_sleep_from
            to_hour = settings.default_joker_sleep_to

        if 0 <= from_hour <= 23 and 0 <= to_hour <= 23:
            joker_settings.update_sleep_interval(chat_id, from_hour, to_hour)
            context.bot.send_message(
                chat_id,
                f'Интервал сна изменен: с {from_hour} до {to_hour} МСК',
            )
        else:
            context.bot.send_message(
                chat_id,
                'Интервал должен быть указан двумя числами от 0 до 23',
            )
    else:
        context.bot.send_message(chat_id, 'Разрешено только админам')


def _is_from_admin(message, bot):
    sender = bot.get_chat_member(message.chat.id, message.from_user.id)
    logging.info(f'Sender: {sender.user.username} {sender.status}')
    return (sender.status in ['creator', 'administrator']) or \
           (sender.user.username in settings.admins)
