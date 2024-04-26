from aiogram.fsm.state import State, StatesGroup


class RemoveAppFSM(StatesGroup):
    """Класс определяющий состояния для процесса удаления приложений."""
    choosing_app = State()


class SubscribeAppFSM(StatesGroup):
    """Класс определяющий состояния для процесса подписки на приложений."""
    choosing_app = State()


class GetLaunchLinkAppFSM(StatesGroup):
    """Класс определяющий состояния для процесса получения ссылок запуска для
    приложений."""
    choosing_app = State()
