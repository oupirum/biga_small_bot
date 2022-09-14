import threading
import time
import random
import requests
from xml.etree import ElementTree
import logging
from telegram.error import Unauthorized

import settings
from app import api
from app import chats
from app.modules.joker import joker_settings


class JokerService(threading.Thread):
    daemon = True

    def __init__(self):
        super().__init__()

    def run(self):
        logging.info('Start joker service')

        while True:
            time.sleep(random.randrange(int(settings.joker_sleep_min), int(settings.joker_sleep_max)))

            active_chats = chats.get_active_list()
            for chat in active_chats:
                chat_id = chat.get('id')
                chat_name = chat.get('name')
                try:
                    last_joke_time, interval = joker_settings.get_timer(chat_id)
                    sleep_from_hour, sleep_to_hour = joker_settings.get_sleep_interval(chat_id)

                    is_interval_passed = time.time() - (last_joke_time or 0) > interval
                    is_not_sleep = not _is_hour_between(
                        time.gmtime().tm_hour + settings.timezone_diff,
                        sleep_from_hour,
                        sleep_to_hour
                    )
                    if is_interval_passed and is_not_sleep:
                        logging.info(f'Run joker for chat {chat_name}')
                        bot = api.create_bot()
                        self._send_joke(chat_id, bot)
                        joker_settings.update_last_joke_time(chat_id, int(time.time()))
                        continue

                except Unauthorized:
                    logging.warning(f'Unauthorized for chat {chat_name}. Deactivating chat.')
                    chats.disable(chat_id)
                except:
                    logging.exception('Joker error')

                time.sleep(1)

    def _send_joke(self, chat_id, bot):
        text = _get_joke(joker_settings.get_types(chat_id))
        logging.info(f'Send joke: {text[0:60]}...')
        bot.send_message(chat_id, text)


def _get_joke(type_ids):
    res = requests.get('http://rzhunemogu.ru/Rand.aspx?CType=%d' % random.choice(type_ids))
    res_tree = ElementTree.fromstring(res.text)
    content = res_tree.find('content')
    return content.text


def _is_hour_between(hour, start_hour, end_hour):
    start = start_hour % 24
    end = (end_hour - start) % 24
    point = (hour + 24 - start) % 24
    return 0 <= point < end
