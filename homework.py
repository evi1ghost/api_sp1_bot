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


PRAKTIKUM_TOKEN = os.getenv('PRAKTIKUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')


def parse_homework_status(homework):
    homework_name = homework.get('homework_name')
    statuses = {
        'reviewing': 'Домашка взата в ревью.',
        'rejected': 'К сожалению в работе нашлись ошибки.',
        'approved': (
            'Ревьюеру всё понравилось, можно приступать к следующему уроку.'
        )
    }
    verdict = statuses.get(homework.get('status'))
    if not verdict or not homework_name:
        raise Warning('Неверный ответ сервера')
    return f'Изменился статус работы "{homework_name}"!\n\n{verdict}'


def get_homework_statuses(current_timestamp):
    headers = {'Authorization': f'OAuth {PRAKTIKUM_TOKEN}'}
    params = {'from_date': current_timestamp}
    try:
        homework_statuses = requests.get(
            'https://praktikum.yandex.ru/api/user_api/homework_statuses/',
            headers=headers,
            params=params
        )
    except requests.RequestException:
        raise Warning('Ошибка сервера')
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
            try:
                send_message(error_message, bot)
            except telegram.error.TelegramError:
                pass
            time.sleep(300)


if __name__ == '__main__':
    main()
