import os
from datetime import datetime
from datetime import timedelta

import pytz
from telethon import TelegramClient, events
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
PERSONAL_CHAT_TYPE = 'PeerUser'

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


@events.register(events.NewMessage(incoming=True))
async def test_replyer(event):
    if is_working_time():
        return

    if not PERSONAL_CHAT_TYPE in str(event.message.peer_id):
        return
        
    user_id = event.message.sender_id
    now_time = datetime.now()
    delta = timedelta(hours=DELAY_HOURS)

    if not user_id in messages_cache:
        messages_cache[user_id] = now_time
        return await event.reply(REPLY)

    should_send_message = (now_time - messages_cache[user_id]) > delta

    if not should_send_message:
        return
    
    messages_cache[user_id] = now_time

    await event.reply(REPLY)

if __name__ == '__main__':
    load_dotenv()

    client = TelegramClient('test_session', api_id=os.environ['TG_API_ID'],
                            api_hash=os.environ['TG_API_HASH'])
    client.start(phone=os.environ['PHONE_NUMBER'])

    with client:
        client.add_event_handler(test_replyer)
        client.run_until_disconnected()

