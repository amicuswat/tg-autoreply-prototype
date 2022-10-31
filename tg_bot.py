import os
from datetime import datetime

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

REPLY = 'Текст ответа'


def is_working_time():
    week_day = datetime.isoweekday(datetime.now())
    if not SHEDULE[week_day]:
        return False
    work_start, work_stop = SHEDULE[week_day].split('-')
    work_start = datetime.strptime(work_start.strip(), '%H:%M').time()
    work_stop = datetime.strptime(work_stop.strip(), '%H:%M').time()
    time_now = datetime.now().time()
    return work_start <= time_now <= work_stop


def replier_handler(update):
    if not update['message']['is_outgoing'] and not is_working_time():
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
