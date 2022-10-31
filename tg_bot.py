import os
from datetime import datetime
from datetime import timedelta

import pytz
from telegram.client import Telegram
from dotenv import load_dotenv

SHEDULE = {
    1: '10:00 - 18:00',
    2: '10:00 - 18:00',
    3: '10:00 - 18:00',
    4: '10:00 - 18:00',
    5: '10:00 - 18:00',
    6: '',
    7: ''}

REPLY = '''
Здравствуйте!). 
В Будни дни с 18:00 до 10:00 утра (МСК) - Ответ будет не таким оперативным.

В субботу и воскресенье - Ответы тоже могут быть не такими быстрыми.

Но не переживайте, мы вам обязательно ответим!
И в будущем ответы будут быстрее, качественнее и без выходных.
'''

DELAY_HOURS = 12

messages_cache = {}


def is_working_time():
    week_day = datetime.isoweekday(datetime.now())
    if not SHEDULE[week_day]:
        return False
    work_start, work_stop = SHEDULE[week_day].split('-')
    work_start = datetime.strptime(work_start.strip(), '%H:%M').time()
    work_stop = datetime.strptime(work_stop.strip(), '%H:%M').time()

    timezone = pytz.timezone(os.environ['TIMEZONE'])
    tz_aware_time = datetime.now().astimezone(timezone).time()

    return work_start <= tz_aware_time <= work_stop



def replier_handler(update):
    if update['message']['is_outgoing']:
        return

    if is_working_time():
        return

    user_id = update['message']['sender_id']['user_id']
    now_time = datetime.now()
    delta = timedelta(hours=DELAY_HOURS)

    if not user_id in messages_cache:
        messages_cache[user_id] = now_time

        chat_id = update['message']['chat_id']
        tg.send_message(chat_id=chat_id, text=REPLY)

        return

    should_send_message = (now_time - messages_cache[user_id]) > delta

    if not should_send_message:
        return

    messages_cache[user_id] = now_time

    chat_id = update['message']['chat_id']

    tg.send_message(chat_id=chat_id, text=REPLY)


if __name__ == '__main__':
    load_dotenv()

    tg = Telegram(
        api_id=os.environ['TG_API_ID'],
        api_hash=os.environ['TG_API_HASH'],
        phone=os.environ['PHONE_NUMBER'],
        database_encryption_key=os.environ['DB_ENCRYPTION_KEY'],
    )
    tg.login()

    # if this is the first run, library needs to preload all chats
    # otherwise the message will not be sent
    tg.add_message_handler(replier_handler)

    tg.idle()
