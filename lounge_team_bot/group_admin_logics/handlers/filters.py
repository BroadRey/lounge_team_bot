from typing import Union

from aiogram import filters, types


class IsGroupChatFilter(filters.BoundFilter):
    async def check(self, event: Union[types.Message, types.CallbackQuery]):
        if isinstance(event, types.Message):
            return event.chat.type != 'private'

        return event.message.chat.type != 'private'
