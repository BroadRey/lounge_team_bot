from aiogram import Bot, Dispatcher
from decouple import Csv, config

TOKEN=config('TOKEN')
ADMINS = config('ADMINS', cast=Csv(post_process=tuple, cast=int))

bot = Bot(token=TOKEN)
dispatcher = Dispatcher(bot)