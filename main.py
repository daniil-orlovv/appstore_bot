import asyncio
import logging

from aiogram import Bot, Dispatcher
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool
from models.models import Base
from handlers import user_handlers, admin_handlers
from config_data.config import Config, load_config
from middlewares.middleware import DBMiddleware

logger = logging.getLogger(__name__)


async def main():
    try:
        logger.info('Starting bot')
        config: Config = load_config()
        bot = Bot(token=config.tg_bot.token)
        db = create_engine(
            'sqlite:///sqlite3.db',
            poolclass=QueuePool,
            pool_size=5,
            max_overflow=10
        )
        Base.metadata.create_all(db)
        dp = Dispatcher()
        dp.workflow_data.update({'db': db, 'config': config})

        dp.include_router(admin_handlers.router)
        dp.include_router(user_handlers.router)

        dp.update.outer_middleware(DBMiddleware())

        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    except Exception as error:
        logger.error(f'Ошибка в работе программы: {error}')

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info('Программа остановлена пользователем вручную')
