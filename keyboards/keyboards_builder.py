from aiogram.types import (KeyboardButton, InlineKeyboardButton,
                           InlineKeyboardMarkup)
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder


def create_inline_kb(adjust: list, *args, **kwargs) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []

    if kwargs:

        for key, value in kwargs.items():
            buttons.append(InlineKeyboardButton(
                    text=key,
                    callback_data=value
                ))

    if args:
        for value in args:
            buttons.append(InlineKeyboardButton(
                        text=f'{value}',
                        callback_data=f'{value}'
            ))

    kb_builder.add(*buttons)
    kb_builder.adjust(*adjust)
    return kb_builder.as_markup(resize_keyboard=True)
