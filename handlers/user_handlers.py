from aiogram.filters import CommandStart, Command
from aiogram import Router
from aiogram.types import Message


router = Router()


@router.message(CommandStart())
async def start(message: Message):
    '''Проверяет ключ пользователя и разрешает/запрещает доступ.'''

    # key_for_start = message.get_args()
    await message.answer('Вы вызвали команду /start')


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
