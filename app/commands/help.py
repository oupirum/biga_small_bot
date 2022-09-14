import telegram

import settings


def help_handler(update, context):
    chat_id = update.effective_chat.id
    context.bot.send_message(
        chat_id,
        f'Мое стоп-слово - /{settings.stop_word}\n'
        '\n'
        'Админские команды:\n'
        '<b>/set_joke_interval N</b>  - изменить интервал постинга шуток. N - число в часах.\n'
        'Например, <b>/set_joke_interval 0.5</b>  - полчаса\n'
        'Интервал по умолчанию - 4 часа.\n'
        '\n'
        '<b>/set_joke_types Typea,Typeb,...</b>  - изменить тип шуток\n'
        'Доступные типы: Joke,Story,Rhyme,Aphorism,Quote,Toast,Status\n'
        '\n'
        '<b>/set_joke_sleep_time N M</b>  - изменить время сна шутника. N, M - часы (0-23)\n'
        'Например, <b>/set_joke_sleep_time 23 10</b> - не постить шутки с 11 вечера до 10 утра\n'
        'Время сна по умолчанию - с полуночи до 9 утра МСК.\n'
        ,
        parse_mode=telegram.ParseMode.HTML
    )
