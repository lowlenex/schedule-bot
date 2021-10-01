import logging
import requests

from os import environ
from dotenv import load_dotenv
from requests.models import Response

from telegram.ext import Updater
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.contexttypes import ContextTypes
from telegram.ext.dispatcher import Dispatcher
from telegram.ext.filters import Filters
from telegram.ext.messagehandler import MessageHandler
from telegram.update import Update

TOKEN: str = ''


def main():
    updater: Updater = Updater(token=TOKEN)
    dispatcher: Dispatcher = updater.dispatcher

    start_handler: CommandHandler = CommandHandler('start', start)

    logging.basicConfig(
        format='%(asctime)s : %(name)s - [%(levelname)s] %(message)s',
        level=logging.INFO
    )

    dispatcher.add_handler(start_handler)

    updater.start_polling()


def start(update: Update, context):
    TIME_API_URL: str = 'http://worldtimeapi.org/api/timezone/Europe/Moscow'
    DAYS_IN_WEEK: dict = {
        1: 'понедельник',
        2: 'вторник',
        3: 'среду',
        4: 'четверг',
        5: 'пятницу',
        6: 'субботу'
    }

    response: Response = requests.get(TIME_API_URL).json()
    week_number: int = int(response['week_number'])
    day_number: int = int(response['day_of_week'])

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f'Расписание на {DAYS_IN_WEEK[day_number]}, {"четная" if week_number % 2 == 0 else "нечетная"} неделя'
    )


load_dotenv()

TOKEN = environ.get('TOKEN')

if __name__ == '__main__':
    main()
