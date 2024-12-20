import asyncio
from bot_config import dp, bot

from handlers.start import start_router
from handlers.picture import picture_router
from handlers.other_messages import other_echo_handler
from handlers.reviews import questions_router
from handlers.admin_module import admin_module
from handlers.table import table



async def main():
    dp.include_router(start_router)
    dp.include_router(picture_router)
    dp.include_router(other_echo_handler)
    dp.include_router(questions_router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())