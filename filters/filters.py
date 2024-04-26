import logging

from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery
from sqlalchemy import Engine

from models.models import App

logger = logging.getLogger(__name__)


class CheckCallbackApp(BaseFilter):
    """Класс для фильтра, определяющего, находится ли приложение в БД или нет.
    """

    async def __call__(
            self,
            callback: CallbackQuery,
            session: Engine
    ) -> bool:
        """Метод выполняющий проверку наличия объекта App в базе данных по
        заданному условию. Если объект есть - возвращает True, инчаче - False
        """

        app = session.query(App).filter(App.title == callback.data).one()
        logger.debug('Filter CheckCallbackApp has worked.')
        if app:
            return True
        return False
