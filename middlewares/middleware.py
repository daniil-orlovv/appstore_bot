from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from sqlalchemy.orm import sessionmaker
from aiogram.types import TelegramObject


class DBMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:

        db = data['db']
        print(db)
        connection = db.connect()
        Session = sessionmaker(bind=db)
        session = Session(bind=connection)
        data['session'] = session

        result = await handler(event, data)

        # ...
        # Здесь выполняется код на выходе из middleware
        # ...

        return result
