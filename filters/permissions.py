import logging

from aiogram.filters import BaseFilter
from aiogram.types import Message

from config_data.config import Config

logger = logging.getLogger(__name__)


class IsAdmin(BaseFilter):
    """Класс-фильтр, определяющий, является ли пользователь администратором
    или нет."""

    async def __call__(self, message: Message, config: Config) -> bool:
        """Проверяет, является ли пользователь, отправивший сообщение,
        администратором."""
        logger.debug('Filter IsAdmin has worked.')
        return message.from_user.id in config.tg_bot.admin_ids
