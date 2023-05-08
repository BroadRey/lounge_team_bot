from aiogram.utils import executor
from config import dispatcher
from group_admin_logic.handlers import command_handlers

if __name__ == '__main__':
    command_handlers.register_command_handlers(dispatcher)
    
    executor.start_polling(dispatcher, skip_updates=True)