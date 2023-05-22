from asyncio import sleep
from typing import Any

import emoji
import requests
from aiogram import Dispatcher, types
from config import ADMINS, WEATHER_TOKEN, bot


def register_command_handlers(dp: Dispatcher):
    dp.register_message_handler(
        weather_command_handler,
        commands=['weather'],
        commands_prefix='/!'
    )


async def weather_command_handler(msg: types.Message):
    msg_validation_result = await is_valid_weather_command(msg)

    if not msg_validation_result['is_valid']:
        if msg_validation_result['content']:
            hint_msg = await msg.answer(msg_validation_result['content'])
            await sleep(3)
            await bot.delete_message(hint_msg.chat.id, hint_msg.message_id)
        return

    weather_emojies = {
        'Thunderstorm': emoji.emojize('Гроза :cloud_with_lightning_and_rain:'),
        'Drizzle': emoji.emojize('Небольшой дождь :sun_behind_rain_cloud:'),
        'Rain': emoji.emojize('Дождь :cloud_with_rain:'),
        'Snow': emoji.emojize('Снег :cloud_with_snow:'),
        'Fog': emoji.emojize('Туман :fog:'),
        'Clear': emoji.emojize('Ясно :sun:'),
        'Clouds': emoji.emojize('Облачно :cloud:'),
    }

    city = msg.get_args().split()[0]
    city = translate(city, 'en')
    weather_response = requests.get(
        'https://api.openweathermap.org/data/2.5/weather'
        f'?q={city}&appid={WEATHER_TOKEN}&units=metric'
    )

    weather_data = weather_response.json()

    city_name = translate(weather_data['name'])
    temp = weather_data['main']['temp']
    weather_description = weather_data['weather'][0]['main']
    humidity = weather_data['main']['humidity']
    pressure = weather_data['main']['pressure']
    wind_speed = weather_data['wind']['speed']

    if weather_description in weather_emojies:
        weather_description = weather_emojies[weather_description]
    else:
        weather_description = 'Дружище, там что-то странное за окном, глянь сам!'

    await msg.reply(
        f'Текущая погода в городе: {city_name}\n'
        f'Температура: {temp}°C | {weather_description}\n'
        f'Влажность: {humidity}%\n'
        f'Давление: {pressure} мм.\n'
        f'Скорость ветра: {wind_speed} м/с'
    )

    await bot.delete_message(msg.chat.id, msg.message_id)


def translate(text, to='ru') -> str:
    from googletrans import Translator
    translator = Translator()
    result = translator.translate(text, dest=to)
    return result.text


async def is_valid_weather_command(msg: types.Message) -> dict[str, Any]:
    async def delete_message():
        return await bot.delete_message(msg.chat.id, msg.message_id)

    if (
        not msg.chat.type == 'private'
        and int(msg.from_user.id) not in ADMINS
    ):
        await delete_message()
        return {
            'is_valid': False,
            'content': '',
        }

    msg_args = msg.get_args()
    right_format_message = (
        'Запрос на получение погоды должен иметь следующий формат:\n'
        '/weather <название_города>'
    )

    if msg_args is None:
        await delete_message()
        return {
            'is_valid': False,
            'content': right_format_message,
        }

    msg_args = msg_args.split()

    if len(msg_args) != 1:
        await delete_message()
        return {
            'is_valid': False,
            'content': right_format_message,
        }

    return {
        'is_valid': True,
        'content': '',
    }
