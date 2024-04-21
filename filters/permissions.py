from aiogram.types import Message
from aiogram.filters import BaseFilter

from config_data.config import Config


class IsAdmin(BaseFilter):
    def __init__(self, config: Config) -> None:
        self.admin_ids = config.tg_bot.admin_ids

    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in self.admin_ids
