from sqlalchemy import Engine
from aiogram.types import CallbackQuery
from aiogram.filters import BaseFilter

from models.models import App


class CheckCallbackApp(BaseFilter):

    async def __call__(
            self,
            callback: CallbackQuery,
            session: Engine
    ) -> bool:

        app = session.query(App).filter(App.title == callback.data).one()
        if app:
            return True
        return False
