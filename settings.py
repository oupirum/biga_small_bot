import os
from dotenv import load_dotenv

load_dotenv()

api_token = os.getenv('API_TOKEN')
admins = os.getenv('ADMINS').split(',')

stop_word = 'FLUGGEGECHEIMEN'

default_joke_types = (
    11,
    12,
    13,
    14,
    15,
    16,
    18
)
joker_sleep_min = 60 * 60 * 0.16
joker_sleep_max = 60 * 60 * 0.66
default_joker_interval = 60 * 60 * 4
default_joker_sleep_from = 0
default_joker_sleep_to = 9
timezone_diff = 3

reply_joseph_session_min_interval = 60 * 60 * 3
reply_joseph_session_length = 2
