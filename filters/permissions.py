from aiogram.filters import BaseFilter
from aiogram.types import Message

from config_data.config import Config


class IsAdmin(BaseFilter):
    """Класс-фильтр, определяющий, является ли пользователь администратором
    или нет.

    Этот класс используется для проверки, является ли пользователь,
    отправивший сообщение, администратором. Он основан на списке
    идентификаторов администраторов, которые хранятся в конфигурации
    приложения."""

    async def __call__(self, message: Message, config: Config) -> bool:
        """Проверяет, является ли пользователь, отправивший сообщение,
        администратором."""
        return message.from_user.id in config.tg_bot.admin_ids
