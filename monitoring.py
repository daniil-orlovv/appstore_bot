import aiohttp
import logging
from sqlalchemy.orm import sessionmaker
from aiogram.exceptions import TelegramForbiddenError

from models.models import App
from utils.utils_db import get_ids_users_from_db

logger = logging.getLogger(__name__)


async def checking_apps(engine, bot):
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
                            message = (f'Приложение {app.title} недоступно по ссылке')
                            for id_user in ids_users:
                                await bot.send_message(id_user, message)
                        else:
                            app.counter += 1
        session.commit()
    except TelegramForbiddenError as e:
        logger.error(f'Пользователь заблокировал бота: {e}')
