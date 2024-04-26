import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

from config_data.config import Config, load_config
from handlers import admin_handlers, user_handlers
from middlewares.middleware import DBMiddleware
from models.models import Base
from utils.utils import checking_apps

logger = logging.getLogger(__name__)


def set_scheduled_jobs(scheduler, engine, bot, config):
    """Устанавливает задачи для планировщика."""

    return scheduler.add_job(
        checking_apps,
        "interval",
        minutes=int(config.interval_value.minutes),
        args=(engine, bot)
    )


async def main():
    """Точка входа в бота."""

    try:
        logger.info('Starting bot')
        config: Config = load_config()
        scheduler = AsyncIOScheduler()
        bot = Bot(
            token=config.tg_bot.token,
            default=DefaultBotProperties(parse_mode=ParseMode.HTML))
        engine = create_engine(
            'sqlite:///sqlite3.db',
            poolclass=QueuePool,
            pool_size=5,
            max_overflow=10
        )
        Base.metadata.create_all(engine)
        dp = Dispatcher()

        dp.include_router(admin_handlers.router)
        dp.include_router(user_handlers.router)

        dp.update.outer_middleware(DBMiddleware())

        job = set_scheduled_jobs(scheduler, engine, bot, config)
        dp.workflow_data.update({
            'db': engine, 'bot': bot, 'config': config, 'job': job,
            'scheduler': scheduler})

        await bot.delete_webhook(drop_pending_updates=True)
        scheduler.start()
        await dp.start_polling(bot)
    except Exception as error:
        logger.error(f'Ошибка в работе программы: {error}')

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info('Программа остановлена пользователем вручную')
