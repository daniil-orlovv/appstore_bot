import logging

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
from lexicon.admin_handlers import (lex_accept_remove, lex_add, lex_broadcast,
                                    lex_generate_key, lex_remove,
                                    lex_set_interval)
from models.models import App
from states.states import RemoveAppFSM
from utils.utils_db import (add_app_to_db, add_key_to_db, check_exist_app,
                            check_exist_key, get_ids_users_from_db,
                            remove_app_from_db)

router = Router()
logger = logging.getLogger(__name__)


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
            await message.answer(lex_add['message'].format(title=title))
        else:
            await message.answer(lex_add['else_message'])
        logger.debug(lex_add['logger_debug'])
    except ValueError:
        await message.answer(lex_add['value_error'])


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
            text=lex_remove['message'],
            reply_markup=inline_keyboard)
        await state.set_state(RemoveAppFSM.choosing_app)
    else:
        await message.answer(lex_remove['else_message'])
        await state.clear()
    logger.debug(lex_remove['logger_debug'])


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
    await callback.message.edit_text(
        text=lex_accept_remove['message'].format(name_app=name_app))
    await state.clear()
    logger.debug(lex_accept_remove['logger_debug'])


@router.message(IsAdmin(), Command('setinterval'))
async def set_interval(message: Message, config: Config,
                       job: Job, scheduler: AsyncIOScheduler):
    """Устанавливает интервал времени для проверки доступности приложения."""

    try:
        cmd, value = message.text.split()
        config.update_interval(value)
        scheduler.reschedule_job(
            job.id, trigger='interval', minutes=int(value))

        await message.answer(lex_set_interval['message'].format(value=value))
    except ValueError:
        await message.answer(lex_set_interval['value_error'])
    logger.debug(lex_set_interval['logger_debug'])


@router.message(IsAdmin(), Command('generatekey'))
async def generate_key(message: Message, session: Session):
    """Генерирует ключ доступа для пользователей."""

    try:
        cmd, key_access = message.text.split()
        if check_exist_key(session, key_access) is True:
            add_key_to_db(session, key_access)
            await message.answer(
                lex_generate_key['message'].format(key_access=key_access))
        else:
            await message.answer(lex_generate_key['else_message'])
    except ValueError:
        await message.answer(lex_generate_key['value_error'])
    logger.debug(lex_generate_key['logger_debug'])


@router.message(IsAdmin(), Command('broadcast'))
async def broadcast(message: Message, session: Session, bot: Bot):
    """Отправляет сообщение всем пользователям."""

    try:
        cmd, text = message.text.split(maxsplit=1)
        ids_users = get_ids_users_from_db(session)
        for id_user in ids_users:
            await bot.send_message(id_user, text)
    except ValueError:
        await message.answer(lex_broadcast['value_error'])
    logger.debug(lex_broadcast['logger_debug'])
