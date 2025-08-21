from aiogram import Bot, Dispatcher
from aiogram.types import ParseMode
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import os
import logging
from helpers import read_file


def setup_logging() -> None:
    """Configure application-wide logging."""
    logging.basicConfig(
        filename='bot_logs.txt',
        filemode='a',
        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
        datefmt='%H:%M:%S',
        level=logging.INFO,
    )


async def on_startup(dp: Dispatcher) -> None:
    """Initialize bot handlers on startup."""
    import handlers

    handlers.setup(dp)

if __name__ == '__main__':
    setup_logging()

    logger = logging.getLogger('BOT_BASE')

    logger.info('startup')
    bot_token = read_file('bot_key')
    if bot_token is None:
        logger.info('havent bot token, stop...')
        exit()
    
    os.makedirs('data', exist_ok=True)
    bot = Bot(bot_token, parse_mode=ParseMode.MARKDOWN_V2, validate_token=True)
    dp = Dispatcher(bot)
    
    try:
        logger.info('started')
        executor.start_polling(dp, on_startup=on_startup)
    finally:
        logger.info('stopped')
