from aiogram import Bot, Dispatcher
from aiogram.types import ParseMode
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import os

async def on_startup(dp: Dispatcher):
    import handlers
    handlers.setup(dp)

def read_file(path):
    with open(path, 'r') as f:
        info = f.read()
        return info
    print('cant read file', path)
    return None

if __name__ == '__main__':
    bot_token = read_file('bot_key')
    if bot_token is None:
        exit() 
    os.makedirs('data', exist_ok=True)
    bot = Bot(bot_token, parse_mode=ParseMode.MARKDOWN_V2, validate_token=True)
    dp = Dispatcher(bot)
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
