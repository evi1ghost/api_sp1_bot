import logging
import os
import time

import requests
import telegram
from dotenv import load_dotenv

load_dotenv()


logging.basicConfig(
    format='%(asctime)s, %(levelname)s, %(name)s, %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p'
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


PRAKTIKUM_TOKEN = os.getenv("PRAKTIKUM_TOKEN")
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')


def parse_homework_status(homework):
    homework_name = homework['homework_name']
    statuses = {
        'reviewing': 'Домашка взатя в ревью.',
        'rejected': 'К сожалению в работе нашлись ошибки.',
        'approved': (
            'Ревьюеру всё понравилось, можно приступать к следующему уроку.'
        )
    }
    verdict = statuses[homework['status']]
    return f'У вас проверили работу "{homework_name}"!\n\n{verdict}'


def get_homework_statuses(current_timestamp):
    headers = {'Authorization': f'OAuth {PRAKTIKUM_TOKEN}'}
    from_date = {'from_date': current_timestamp}
    homework_statuses = requests.get(
        'https://praktikum.yandex.ru/api/user_api/homework_statuses/',
        headers=headers,
        params=from_date
    )
    return homework_statuses.json()


def send_message(message, bot_client):
    logger.info('Message sent')
    return bot_client.send_message(CHAT_ID, message)


def main():
    logger.debug('Bot started')
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    current_timestamp = int(time.time())

    while True:
        try:
            new_homework = get_homework_statuses(current_timestamp)
            if new_homework.get('homeworks'):
                send_message(
                    parse_homework_status(new_homework.get('homeworks')[0]),
                    bot
                )
            current_timestamp = new_homework.get(
                'current_date', current_timestamp
            )
            time.sleep(300)

        except Exception as e:
            error_message = f'Бот столкнулся с ошибкой: {e}'
            logger.error(error_message)
            send_message(error_message, bot)
            time.sleep(5)


if __name__ == '__main__':
    main()
