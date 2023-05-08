import datetime
from asyncio import sleep

from aiogram import Dispatcher, types
from config import ADMINS, bot

from .filters import IsGroupChatFilter


def register_command_handlers(dp: Dispatcher):
    dp.register_message_handler(
        mute_command_handler,
        IsGroupChatFilter(),
        commands=['mute'],
        commands_prefix='/!'
    )


async def mute_command_handler(msg: types.Message):
    await bot.delete_message(msg.chat.id, msg.message_id)

    if int(msg.from_user.id) not in ADMINS:
        return

    if not msg.reply_to_message:
        not_reply_message = await bot.send_message(
            msg.chat.id,
            'Команда может быть только ответом на сообщение!',
            disable_notification=True
        )
        await sleep(2)
        await bot.delete_message(msg.chat.id, not_reply_message.message_id)
        return``

    chat_member = await bot.get_chat_member(msg.chat.id, msg.reply_to_message.from_user.id)
    member_name = (
        f'@{chat_member.user.username}'
        if chat_member.user.username
        else chat_member.user.full_name
    )

    if chat_member.status == 'restricted':
        yet_restricter_message = await bot.send_message(
            msg.chat.id,
            f'{member_name} уже с кляпом во рту!',
            disable_notification=True
        )
        await sleep(2)
        await bot.delete_message(msg.chat.id, yet_restricter_message.message_id)
        return

    dice_result = await bot.send_dice(msg.chat.id)
    mute_minutes = dice_result.dice.value * 2
    unmute_time = datetime.timedelta(minutes=mute_minutes)

    await bot.restrict_chat_member(
        msg.chat.id,
        chat_member,
        types.ChatPermissions(can_send_messages=False),
        until_date=unmute_time
    )

    await sleep(3)

    await dice_result.reply(
        f'Игральная кость решила судьбу {member_name}!\n'
        f'Ему вставили кляп на следующее количество минут: <b>{mute_minutes}</b>',
        parse_mode=types.ParseMode.HTML,
        disable_notification=True
    )

    await bot.delete_message(msg.chat.id, dice_result.message_id)
