import asyncio

from loguru import logger

from src.handlers.user_handler import register_handlers
from src.misc import bot, dp


async def main():
    register_handlers(dp)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logger.info("Starting bot")
    asyncio.run(main())
