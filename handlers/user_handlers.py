from aiogram.filters import CommandStart, Command
from aiogram import Router
from aiogram.types import Message
from sqlalchemy import Engine

from utils.utils_db import (check_access_for_user, check_exist_user,
                            add_user_to_db, remove_key_from_db)


router = Router()


@router.message(CommandStart())
async def start(message: Message, session: Engine):
    '''Проверяет ключ пользователя и разрешает/запрещает доступ.'''

    try:
        cmd, key = message.text.split()
        if not key:
            await message.answer('Для доступа к боту необходимо указать ключ, '
                                 'который необходимо получить у '
                                 'администратора')
        if check_access_for_user(session, key):
            id_telegram = message.from_user.id
            name = message.from_user.first_name
            data = {'id_telegram': id_telegram, 'name': name}
            if not check_exist_user(session, id_telegram):
                add_user_to_db(session, data)
            await message.answer('Доступ получен.')
            remove_key_from_db(session, key)
        else:
            await message.answer('Введен неверный ключ доступа! '
                                 'Обратитесь к администратору.')
    except ValueError:
        await message.answer('Необходимо указать ключ доступа через пробел '
                             'после команды:'
                             '\n\n<code>/start *значение*</code>')


@router.message(Command('status'))
async def status():
    '''Отправляет статус приложений, находящихся под мониторингом.'''

    pass


@router.message(Command('subscribe'))
async def subscribe():
    '''Создает подписку юзеров на получение уведомлений об изменении статуса
    конкретного приложения.
    '''

    pass


@router.message(Command('getlaunchlinks'))
async def get_launch_links():
    '''Отправляет ссылки для запуска приложения.'''

    pass
