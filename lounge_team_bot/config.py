from aiogram import Bot, Dispatcher
from decouple import Csv, config

BOT_TOKEN=config('BOT_TOKEN')
WEATHER_TOKEN=config('WEATHER_TOKEN')
ADMINS = config('ADMINS', cast=Csv(post_process=tuple, cast=int))

bot = Bot(token=BOT_TOKEN)
dispatcher = Dispatcher(bot)