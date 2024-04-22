from aiogram.fsm.state import State, StatesGroup


class RemoveAppFSM(StatesGroup):
    choosing_app = State()


class SubscribeAppFSM(StatesGroup):
    choosing_app = State()
