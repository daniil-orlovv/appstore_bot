from aiogram.types import CallbackQuery
from aiogram.filters import BaseFilter
from aiogram.fsm.context import FSMContext


class CheckApps(BaseFilter):

    async def __call__(
            self,
            callback: CallbackQuery,
            state: FSMContext
    ) -> bool:

        state_data = await state.get_data()
        return callback.data in state_data['names_apps']
