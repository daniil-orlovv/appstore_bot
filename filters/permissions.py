import logging

from aiogram.filters import BaseFilter
from aiogram.types import Message
from sqlalchemy.orm import Session

from config_data.config import Config
from utils.utils_db import check_exist_user

logger = logging.getLogger(__name__)


class IsAdmin(BaseFilter):
    """Класс-фильтр, определяющий, является ли пользователь администратором
    или нет."""

    async def __call__(self, message: Message, config: Config) -> bool:
        """Проверяет, является ли пользователь, отправивший сообщение,
        администратором."""

        logger.debug('Filter IsAdmin has worked.')
        return message.from_user.id in config.tg_bot.admin_ids


class IsAuth(BaseFilter):
    """Класс-фильтр, определяющий, авторизован ли пользователь с помощью кода
    или нет."""

    async def __call__(self, message: Message, config: Config,
                       session: Session) -> bool:
        """Проверяет, авторизован ли пользователь, отправивший сообщение."""

        logger.debug('Filter IsAuth has worked.')
        return check_exist_user(session, message.from_user.id)
