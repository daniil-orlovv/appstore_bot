from aiogram import Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery, Message
from sqlalchemy import Engine

from filters.filters import CheckCallbackApp
from keyboards.keyboards_builder import create_inline_kb
from states.states import GetLaunchLinkAppFSM, SubscribeAppFSM
from utils.utils import check_access_apps_subscribe
from utils.utils_db import (add_user_to_db, check_access_for_user,
                            check_exist_user, create_subscribe_on_app,
                            get_apps_from_db, get_subscribing_apps_of_user,
                            remove_key_from_db, return_launch_links)

router = Router()


@router.message(CommandStart())
async def start(message: Message, session: Engine):
    """Проверяет ключ пользователя и разрешает/запрещает доступ."""

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
async def status(message: Message, session: Engine):
    """Отправляет статус приложений, находящихся под мониторингом."""

    user_id = message.from_user.id
    dict_urls = get_subscribing_apps_of_user(session, user_id)
    apps_ok, apps_not_found = await check_access_apps_subscribe(
        dict_urls, session)

    ok_message = "Доступные приложения:\n\n"
    for title_app, url in apps_ok.items():
        ok_message += f"{title_app}: {url}\n\n"
    await message.answer(ok_message)

    not_found_message = "Недоступные приложения:\n\n"
    for title_app, url in apps_not_found.items():
        not_found_message += f"{title_app}: {url}\n\n"
    await message.answer(not_found_message)


@router.message(Command('subscribe'), StateFilter(default_state))
async def subscribe(message: Message, session: Engine, state: FSMContext):
    """Отправляет список приложений для выбора, чтобы подписаться на выбранное
    приложение."""

    names_apps = get_apps_from_db(session)
    adjust = (2, 2, 2)
    keyboard = create_inline_kb(adjust, *names_apps)
    if names_apps:
        await message.answer(
            text='На какое приложение нужно подписаться?',
            reply_markup=keyboard)
        await state.set_state(SubscribeAppFSM.choosing_app)
    else:
        await message.answer('Приложений для мониторинга нет.')
        await state.clear()


@router.callback_query(StateFilter(SubscribeAppFSM.choosing_app),
                       CheckCallbackApp())
async def accept_subscribe(callback: CallbackQuery, session: Engine,
                           state: FSMContext):
    """Создает подписку юзеров на получение уведомлений об изменении статуса
    конкретного приложения."""

    title = callback.data
    user_id = callback.from_user.id
    result = create_subscribe_on_app(session, title, user_id)
    await callback.message.edit_text(text=result)
    await state.clear()


@router.message(Command('getlaunchlinks'), StateFilter(default_state))
async def get_launch_links(message: Message, session: Engine,
                           state: FSMContext):
    """Отправляет список приложений для выбора, чтобы получить ссылку для
    запуска."""

    titles_apps = get_apps_from_db(session)
    adjust = (2, 2, 2)
    keyboard = create_inline_kb(adjust, *titles_apps)

    if titles_apps:
        await message.answer(
            text='Для какого приложения получить ссылку для запуска?',
            reply_markup=keyboard)
        await state.set_state(GetLaunchLinkAppFSM.choosing_app)
    else:
        await message.answer('Приложений для мониторинга нет.')
        await state.clear()


@router.callback_query(StateFilter(GetLaunchLinkAppFSM.choosing_app),
                       CheckCallbackApp())
async def accept_get_launch_links(callback: CallbackQuery, session: Engine,
                                  state: FSMContext):
    """Отправляет ссылку для запуска выбранного приложения."""

    title = callback.data
    url_app = return_launch_links(session, title)
    await callback.message.edit_text(
        text=f'Ссылка для запуска {title}: {url_app}')
    await state.clear()
