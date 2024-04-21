from aiogram.filters import Command
from aiogram import Router
from aiogram.types import Message, CallbackQuery
from sqlalchemy import Engine
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

from utils.utils_db import (add_app_to_db, add_key_to_db, remove_app_from_db,
                            check_exist_app, check_exist_key,
                            get_ids_users_from_db)
from models.models import App
from keyboards.keyboards_builder import create_inline_kb
from states.states import RemoveAppFSM
from filters.filters import CheckApps
from filters.permissions import IsAdmin
from config_data.config import load_config

router = Router()
config = load_config()


@router.message(
        IsAdmin(config),
        StateFilter(default_state),
        Command(commands='add')
)
async def add(message: Message, session: Engine):
    '''Добавляет URL приложения для мониторинга.'''

    try:
        url, title, launch_url = message.text.split()[1:]
        data = {'title': title, 'url': url, 'launch_url': launch_url}

        if check_exist_app(session, data) is True:
            add_app_to_db(session, data)
            await message.answer(
                f"Приложение {title} добавлено для мониторинга.")
        else:
            await message.answer(
                'Такое приложение уже существует!')
    except ValueError:
        await message.answer('Необходимо указать url, название и ссылку для '
                             'запуска через пробел после команды: \n\n'
                             '<code>/add url title launch_url</code>')


@router.message(IsAdmin(config), StateFilter(default_state), Command('remove'))
async def remove(message: Message, session: Engine, state: FSMContext):
    '''Удаляет URL приложения для мониторинга.'''

    all_apps = session.query(App.id, App.title).all()
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
        await message.answer('Приложений для мониторинга нет.')
        await state.clear()


@router.callback_query(
        IsAdmin(config),
        StateFilter(RemoveAppFSM.choosing_app),
        CheckApps()
)
async def accept_remove(
    callback: CallbackQuery,
    session: Engine,
    state: FSMContext
):
    '''Подтверждение удаления.'''

    name_app = callback.data
    remove_app_from_db(session, name_app)
    await callback.message.edit_text(text=f'Приложение {name_app} удалено!')
    await state.clear()


@router.message(IsAdmin(config), Command('setinterval'))
async def set_interval(message: Message, config):
    '''Устанавливает интервал времени для проверки доступности приложения.'''

    try:
        cmd, value = message.text.split()
        config.update_interval(value)
        await message.answer(
            f'Интервал времени для проверки установлен: {value} минут')
    except ValueError:
        await message.answer('Необходимо указать значение интервала через '
                             'пробел после команды в минутах:'
                             '\n\n<code>/setinterval *значение*</code>')


@router.message(IsAdmin(config), Command('generatekey'))
async def generate_key(message: Message, session: Engine):
    '''Генерирует ключ доступа для пользователей.'''

    try:
        cmd, key_access = message.text.split()
        if check_exist_key(session, key_access) is True:
            add_key_to_db(session, key_access)
            await message.answer(f'Ключ доступа создан: {key_access}')
        else:
            await message.answer('Такой ключ уже существует!')
    except ValueError:
        await message.answer('Необходимо указать ключ доступа через пробел '
                             'после команды:'
                             '\n\n<code>/generatekey *значение*</code>')


@router.message(IsAdmin(config), Command('broadcast'))
async def broadcast(message: Message, session: Engine, bot):
    '''Отправляет сообщение всем пользователям.'''

    try:
        cmd, text = message.text.split()
        ids_users = get_ids_users_from_db(session)
        for id_user in ids_users:
            await bot.send_message(id_user, text)
    except ValueError:
        await message.answer('Необходимо указать текст через пробел '
                             'после команды:'
                             '\n\n<code>/broadcast *значение*</code>')
