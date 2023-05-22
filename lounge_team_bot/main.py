import general_chats_logics.handlers.command_handlers as general_handlers
import group_admin_logics.handlers.command_handlers as group_admin_handlers
from aiogram.utils import executor
from config import dispatcher

if __name__ == '__main__':
    group_admin_handlers.register_command_handlers(dispatcher)
    general_handlers.register_command_handlers(dispatcher)
    
    executor.start_polling(dispatcher, skip_updates=True)