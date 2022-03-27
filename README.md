# Telegram-bot
[![Telegram](https://img.shields.io/badge/-Telegram-464646?style=flat-square&logo=Telegram)](https://pypi.org/project/python-telegram-bot/)
[![Heroku](https://img.shields.io/badge/-Heroku-464646?style=flat-square&logo=Heroku)](https://www.heroku.com/)

Данный бот оповещает пользователя об изменении статуса проверки проектной работы. В случаи ошибки, пришлет исключение сообщением в чат.
Для деплоя на [Heroku](https://www.heroku.com/) в репозитории есть Procfile.

## Переменные окружения:  
* `PRAKTIKUM_TOKEN` токен аутентификации Яндекс.Практикума
* `TELEGRAM_TOKEN` телеграмм токен созданного вами бота
* `TELEGRAM_CHAT_ID` id чата с вами

*Токен к API Яндекс Практикума можно получить по адресу: https://oauth.yandex.ru/authorize?response_type=token&client_id=<client_id>, где client_id - id пользователя*
