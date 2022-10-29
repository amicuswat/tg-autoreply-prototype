import os
from datetime import datetime

from telegram.client import Telegram
from dotenv import load_dotenv


SHEDULE = {
    1: '8:00 - 18:00',
    2: '8:00 - 18:00',
    3: '8:00 - 18:00',
    4: '',
    5: '18:00 - 22:00',
    6: '',
    7: ''}


def is_working_time():
    week_day = datetime.isoweekday(datetime.now())
    if not SHEDULE[week_day]:
        return False
    work_start, work_stop = SHEDULE[week_day].split('-')
    work_start = datetime.strptime(work_start.strip(), '%H:%M').time()
    work_stop = datetime.strptime(work_stop.strip(), '%H:%M').time()
    time_now = datetime.now().time()
    if work_start <= time_now and work_stop >= time_now:
        return True
    else:
        return False


def replier_handler(update):
    if not is_working_time():
        chat_id = update['message']['chat_id']
        if update['message']['content'].get('text'):
            message_text = update['message']['content']['text'].get('text')
        else:
            message_text = ''
        reply = 'Занят, отвечу позже.'
        if message_text and message_text.lower() != reply.lower():
            tg.send_message(chat_id=chat_id, text=reply)


if __name__ == '__main__':
    load_dotenv()

    tg = Telegram(
        api_id=os.getenv('TG_API_ID'),
        api_hash=os.getenv('TG_API_HASH'),
        phone=os.getenv('PHONE_NUMBER'),
        database_encryption_key=os.getenv('DB_ENCRYPTION_KEY'),
    )
    tg.login()

    # if this is the first run, library needs to preload all chats
    # otherwise the message will not be sent
    tg.add_message_handler(replier_handler)

    tg.idle()
