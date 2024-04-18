from aiogram.filters import Command
from aiogram import Router
from aiogram.types import Message
from sqlalchemy.orm import sessionmaker

from utils.utils_db import create_app_for_db
from models.models import App

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

    await message.answer(f"Приложение {title} добавлено для мониторинга.")


@router.message(Command('remove'))
async def remove(message: Message, db):
    '''Удаляет URL приложения для мониторинга.'''

    connection = db.connect()
    Session = sessionmaker(bind=db)
    session = Session(bind=connection)
    print(session.query(App.id, App.title).all())  # Получение всех приложений
    i = session.query(App).filter(App.title == 'Название').one()  # Удаление выбранного приложения
    session.delete(i)
    session.commit()


@router.message(Command('setinterval'))
async def set_interval(message: Message, config):
    '''Устанавливает интервал времени для проверки доступности приложения.'''

    value = message.text.split()[1]
    config.update_interval(value)
    await message.answer(f'Интервал времени для проверки установлен: {value} минут')
    print(config.interval_value.minutes)


@router.message(Command('generatekey'))
async def generate_key(message: Message):
    '''Генерирует ключ доступа для пользователей.'''

    pass


@router.message(Command('broadcast'))
async def broadcast(message: Message):
    '''Отправляет сообщение всем пользователям.'''

    pass
