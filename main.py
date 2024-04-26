import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from apscheduler.job import Job
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy import Engine, create_engine
from sqlalchemy.pool import QueuePool

from config_data.config import Config, load_config
from handlers import admin_handlers, user_handlers
from middlewares.middleware import DBMiddleware
from models.models import Base
from utils.utils import checking_apps

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.DEBUG,
    format='[{asctime}] #{levelname:8} {filename}:'
           '{lineno} - {name} - {message}',
    style='{'
)


def set_scheduled_jobs(scheduler: AsyncIOScheduler, engine: Engine, bot: Bot,
                       config: Config) -> Job:
    """Устанавливает задачи для планировщика."""

    logger.debug('func. set_scheduled_jobs has worked.')
    return scheduler.add_job(
        checking_apps,
        "interval",
        minutes=int(config.interval_value.minutes),
        args=(engine, bot)
    )


async def main() -> None:
    """Точка входа в бота."""

    try:
        logger.debug('Starting bot...')
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
        logger.debug('Bot started')
    except Exception as error:
        logger.error(f'Ошибка в работе программы: {error}', exc_info=True)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info('Bot has stopped by admin')
