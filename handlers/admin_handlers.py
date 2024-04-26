from aiogram import Bot, Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery, Message
from apscheduler.job import Job
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy import Engine
from sqlalchemy.orm import Session

from config_data.config import Config
from filters.filters import CheckCallbackApp
from filters.permissions import IsAdmin
from keyboards.keyboards_builder import create_inline_kb
from models.models import App
from states.states import RemoveAppFSM
from utils.utils_db import (add_app_to_db, add_key_to_db, check_exist_app,
                            check_exist_key, get_ids_users_from_db,
                            remove_app_from_db)

router = Router()


@router.message(
        IsAdmin(),
        StateFilter(default_state),
        Command(commands='add')
)
async def add(message: Message, session: Engine):
    """Добавляет URL приложения для мониторинга."""

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


@router.message(IsAdmin(), StateFilter(default_state), Command('remove'))
async def remove(message: Message, session: Session, state: FSMContext):
    """Отправляет кнопки с приложениям для удаления."""

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
        IsAdmin(),
        StateFilter(RemoveAppFSM.choosing_app),
        CheckCallbackApp()
)
async def accept_remove(
    callback: CallbackQuery,
    session: Session,
    state: FSMContext
):
    """Удаляет выбранное приложение."""

    name_app = callback.data
    remove_app_from_db(session, name_app)
    await callback.message.edit_text(text=f'Приложение {name_app} удалено!')
    await state.clear()


@router.message(IsAdmin(), Command('setinterval'))
async def set_interval(message: Message, config: Config,
                       job: Job, scheduler: AsyncIOScheduler):
    """Устанавливает интервал времени для проверки доступности приложения."""

    try:
        cmd, value = message.text.split()
        config.update_interval(value)
        scheduler.reschedule_job(
            job.id, trigger='interval', minutes=int(value))

        await message.answer(
            f'Интервал времени для проверки установлен: {value} минут')
    except ValueError:
        await message.answer('Необходимо указать значение интервала через '
                             'пробел после команды в минутах:'
                             '\n\n<code>/setinterval *значение*</code>')


@router.message(IsAdmin(), Command('generatekey'))
async def generate_key(message: Message, session: Session):
    """Генерирует ключ доступа для пользователей."""

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


@router.message(IsAdmin(), Command('broadcast'))
async def broadcast(message: Message, session: Session, bot: Bot):
    """Отправляет сообщение всем пользователям."""

    try:
        cmd, text = message.text.split(maxsplit=1)
        ids_users = get_ids_users_from_db(session)
        for id_user in ids_users:
            await bot.send_message(id_user, text)
    except ValueError:
        await message.answer('Необходимо указать текст через пробел '
                             'после команды:'
                             '\n\n<code>/broadcast *значение*</code>')
