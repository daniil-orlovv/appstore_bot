import logging

import aiohttp
from aiogram import Bot
from aiogram.exceptions import TelegramForbiddenError
from sqlalchemy import Engine
from sqlalchemy.orm import Session, sessionmaker

from models.models import App
from utils.utils_db import get_ids_users_from_db

logger = logging.getLogger(__name__)


async def check_access_apps_subscribe(dict_urls: dict,
                                      session: Session) -> dict:
    """Проверяет доступность приложений, на которые пользователь подписан."""

    apps_ok = {}
    apps_not_found = {}
    for id, url in dict_urls.items():
        async with aiohttp.ClientSession() as session_http:
            async with session_http.get(url) as resp:
                if resp.status == 200:
                    title_app = session.query(
                        App.title).filter(App.id == id).scalar()
                    apps_ok[title_app] = url
                else:
                    title_app = session.query(
                        App.title).filter(App.id == id).scalar()
                    apps_not_found[title_app] = url
    logger.debug('func. check_access_apps_subscibe has worked.')
    return apps_ok, apps_not_found


async def checking_apps(engine: Engine, bot: Bot) -> None:
    """Проверяет доступность всех приложенй."""

    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        q = session.query(App)

        for app in q:
            async with aiohttp.ClientSession() as session_http:
                async with session_http.get(app.url) as resp:
                    print(resp.status)
                    if resp.status == 200:
                        app.counter = 0
                    else:
                        if app.counter > 3:
                            app.counter = 0
                            ids_users = get_ids_users_from_db(session)
                            message = (
                                f'Приложение {app.title} недоступно по ссылке')
                            for id_user in ids_users:
                                await bot.send_message(id_user, message)
                        else:
                            app.counter += 1
        session.commit()
        logger.debug('func. checking_apps has worked.')
    except TelegramForbiddenError as e:
        logger.error(f'Пользователь заблокировал бота: {e}', exc_info=True)
