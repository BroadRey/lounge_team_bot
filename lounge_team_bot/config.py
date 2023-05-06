from asyncore import dispatcher
from decouple import config
from aiogram import Bot, Dispatcher

TOKEN=config('TOKEN')

bot = Bot(token=TOKEN)
dispatcher = Dispatcher(bot)