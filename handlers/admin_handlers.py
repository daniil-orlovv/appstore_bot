from aiogram.filters import Command
from aiogram import Router
from aiogram.types import Message, CallbackQuery
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Engine
from aiogram.filters import StateFilter, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

from utils.utils_db import (add_app_to_db, add_key_to_db, remove_from_db,
                            check_unique_app, check_key_access)
from models.models import App
from middlewares.middleware import DBMiddleware
from keyboards.keyboards_builder import create_inline_kb
from states.states import RemoveAppFSM
from filters.filters import CheckApps

router = Router()
router.message.outer_middleware(DBMiddleware())


@router.message(StateFilter(default_state), Command(commands='add'))
async def add(message: Message, session: Engine):
    '''Добавляет URL приложения для мониторинга.'''

    url, title, launch_url = message.text.split()[1:]
    data = {'title': title, 'url': url, 'launch_url': launch_url}

    if check_unique_app(session, data) is True:
        add_app_to_db(session, data)
        await message.answer(f"Приложение {title} добавлено для мониторинга.")
    else:
        await message.answer(
            'Такое приложение уже существует!')


@router.message(StateFilter(default_state), Command('remove'))
async def remove(message: Message, session: Engine, state: FSMContext):
    '''Удаляет URL приложения для мониторинга.'''

    all_apps = session.query(App.id, App.title).all()  # Получение всех приложений
    names_apps = [x[-1] for x in all_apps]
    await state.update_data(names_apps=names_apps)
    adjust = [2, 2, 2, 2]
    inline_keyboard = create_inline_kb(adjust, *names_apps)
    if all_apps:
        await message.answer(
            text='Какое приложение необходимо удалить?',
            reply_markup=inline_keyboard)
        await state.set_state(RemoveAppFSM.choosing_app)
    else:
        await message.answer('Приложений для мониторинга нет!')
        await state.clear()


@router.callback_query(StateFilter(RemoveAppFSM.choosing_app), CheckApps())
async def accept_remove(callback: CallbackQuery, session: Engine, state: FSMContext):
    '''Удаляет URL приложения для мониторинга.'''

    name_app = callback.data
    remove_from_db(session, name_app)
    await callback.message.edit_text(text=f'Приложение {name_app} удалено!')
    await state.clear()


@router.message(Command('setinterval'))
async def set_interval(message: Message, config):
    '''Устанавливает интервал времени для проверки доступности приложения.'''

    value = message.text.split()[1]
    config.update_interval(value)
    await message.answer(f'Интервал времени для проверки установлен: {value} минут')
    print(config.interval_value.minutes)


@router.message(Command('generatekey'))
async def generate_key(message: Message, session: Engine):
    '''Генерирует ключ доступа для пользователей.'''

    key_access = message.text.split()[1:]
    if check_key_access(session, *key_access) is True:
        add_key_to_db(session, *key_access)
        await message.answer(f'Ключ доступа создан: {key_access}')
    else:
        await message.answer('Такой ключ уже создан!')


@router.message(Command('broadcast'))
async def broadcast(message: Message):
    '''Отправляет сообщение всем пользователям.'''

    pass
