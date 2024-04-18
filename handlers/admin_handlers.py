from aiogram.filters import Command
from aiogram import Router
from aiogram.types import Message
from sqlalchemy.orm import sessionmaker

from utils.utils_db import create_app_for_db

router = Router()


@router.message(Command(commands='add'))
async def add(message: Message, db):
    '''Добавляет URL приложения для мониторинга.'''

    cmd, url, title, launch_url = message.text.split()
    data = {
        'title': title, 'url': url, 'launch_url': launch_url}
    print(data)

    connection = db.connect()
    Session = sessionmaker(bind=db)
    session = Session(bind=connection)
    object_for_db = create_app_for_db(data)
    session.add(object_for_db)
    session.commit()

    await message.answer(f"Вы вызвали команду {cmd} с аргументами: {url} {title} {launch_url}")


@router.message(Command('remove'))
async def remove(message: Message):
    '''Удаляет URL приложения для мониторинга.'''

    pass


@router.message(Command('/setinterval'))
async def set_interval(message: Message):
    '''Устанавливает интервал времени для проверки доступноси приложения.'''

    pass


@router.message(Command('generatekey'))
async def generate_key(message: Message):
    '''Генерирует ключ доступа для пользователей.'''

    pass


@router.message(Command('broadcast'))
async def broadcast(message: Message):
    '''Отправляет сообщение всем пользователям.'''

    pass
