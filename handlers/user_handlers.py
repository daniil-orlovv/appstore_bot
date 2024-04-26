import logging

from aiogram import Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery, Message
from sqlalchemy.orm import Session

from filters.filters import CheckCallbackApp
from keyboards.keyboards_builder import create_inline_kb
from lexicon.user_handlers import (lex_accept_get_launch_links,
                                   lex_accept_subscribe, lex_get_launch_links,
                                   lex_start, lex_status, lex_subscribe)
from states.states import GetLaunchLinkAppFSM, SubscribeAppFSM
from utils.utils import check_access_apps_subscribe
from utils.utils_db import (add_user_to_db, check_access_for_user,
                            check_exist_user, create_subscribe_on_app,
                            get_apps_from_db, get_subscribing_apps_of_user,
                            remove_key_from_db, return_launch_links)

router = Router()
logger = logging.getLogger(__name__)


@router.message(CommandStart())
async def start(message: Message, session: Session):
    """Проверяет ключ пользователя и разрешает/запрещает доступ."""

    try:
        cmd, key = message.text.split()
        if not key:
            await message.answer(lex_start['not_key'])
        if check_access_for_user(session, key):
            id_telegram = message.from_user.id
            name = message.from_user.first_name
            data = {'id_telegram': id_telegram, 'name': name}
            if not check_exist_user(session, id_telegram):
                add_user_to_db(session, data)
            await message.answer(lex_start['message'])
            remove_key_from_db(session, key)
        else:
            await message.answer(lex_start['else_message'])
    except ValueError:
        await message.answer(lex_start['value_error'])
    logger.debug(lex_start['logger_debug'])


@router.message(Command('status'))
async def status(message: Message, session: Session):
    """Отправляет статус приложений, находящихся под мониторингом."""

    user_id = message.from_user.id
    dict_urls = get_subscribing_apps_of_user(session, user_id)
    apps_ok, apps_not_found = await check_access_apps_subscribe(
        dict_urls, session)

    ok_message = lex_status['ok_message']
    for title_app, url in apps_ok.items():
        ok_message += f"{title_app}: {url}\n\n"
    await message.answer(ok_message)

    not_found_message = lex_status['not_found_message']
    for title_app, url in apps_not_found.items():
        not_found_message += f"{title_app}: {url}\n\n"
    await message.answer(not_found_message)
    logger.debug(lex_status['logger_debug'])


@router.message(Command('subscribe'), StateFilter(default_state))
async def subscribe(message: Message, session: Session, state: FSMContext):
    """Отправляет список приложений для выбора, чтобы подписаться на выбранное
    приложение."""

    names_apps = get_apps_from_db(session)
    adjust = (2, 2, 2)
    keyboard = create_inline_kb(adjust, *names_apps)
    if names_apps:
        await message.answer(
            text=lex_subscribe['message'],
            reply_markup=keyboard)
        await state.set_state(SubscribeAppFSM.choosing_app)
    else:
        await message.answer(lex_subscribe['else_message'])
        await state.clear()
    logger.debug(lex_subscribe['logger_debug'])


@router.callback_query(StateFilter(SubscribeAppFSM.choosing_app),
                       CheckCallbackApp())
async def accept_subscribe(callback: CallbackQuery, session: Session,
                           state: FSMContext):
    """Создает подписку юзеров на получение уведомлений об изменении статуса
    конкретного приложения."""

    title = callback.data
    user_id = callback.from_user.id
    result = create_subscribe_on_app(session, title, user_id)
    await callback.message.edit_text(text=result)
    await state.clear()
    logger.debug(lex_accept_subscribe['logger_debug'])


@router.message(Command('getlaunchlinks'), StateFilter(default_state))
async def get_launch_links(message: Message, session: Session,
                           state: FSMContext):
    """Отправляет список приложений для выбора, чтобы получить ссылку для
    запуска."""

    titles_apps = get_apps_from_db(session)
    adjust = (2, 2, 2)
    keyboard = create_inline_kb(adjust, *titles_apps)

    if titles_apps:
        await message.answer(
            text=lex_get_launch_links['message'],
            reply_markup=keyboard)
        await state.set_state(GetLaunchLinkAppFSM.choosing_app)
    else:
        await message.answer(lex_get_launch_links['else_message'])
        await state.clear()
    logger.debug(lex_get_launch_links['logger_debug'])


@router.callback_query(StateFilter(GetLaunchLinkAppFSM.choosing_app),
                       CheckCallbackApp())
async def accept_get_launch_links(callback: CallbackQuery, session: Session,
                                  state: FSMContext):
    """Отправляет ссылку для запуска выбранного приложения."""

    title = callback.data
    url_app = return_launch_links(session, title)
    await callback.message.edit_text(
        text=lex_accept_get_launch_links['message'].format(
            title=title, url_app=url_app))
    await state.clear()
    logger.debug(lex_accept_get_launch_links['logger_debug'])
