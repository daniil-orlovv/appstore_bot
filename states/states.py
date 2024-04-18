from aiogram.fsm.state import State, StatesGroup


class RemoveAppFSM(StatesGroup):
    choosing_app = State()
    accept_remove = State()
