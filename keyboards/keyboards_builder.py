import logging

from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           KeyboardButton)
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

logger = logging.getLogger(__name__)


def create_inline_kb(adjust: list, *args, **kwargs) -> InlineKeyboardMarkup:
    """Создает инлайн-клавиатуру, принимая аргументы для названия и коллбэка
    кнопок."""
    try:
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
        logger.debug('Inline-keyboard builder has worked.')
        return kb_builder.as_markup(resize_keyboard=True)

    except TypeError as e:
        logger.error(f"Ошибка при создании инлайн-клавиатуры: {e}")
        raise
    except ValueError as e:
        logger.error(f"Ошибка при создании инлайн-клавиатуры: {e}")
        raise
    except Exception as e:
        logger.error(f"Неизвестная ошибка при создании инлайн-клавиатуры: {e}")
        raise


def create_kb(*args) -> InlineKeyboardMarkup:
    """Создает клавиатуру, принимая аргументы для названия кнопок."""
    try:
        kb_builder = ReplyKeyboardBuilder()
        buttons: list[KeyboardButton] = []

        for value in args:
            buttons.append(KeyboardButton(
                    text=value
                ))
        kb_builder.row(*buttons, width=1)
        return kb_builder.as_markup(resize_keyboard=True)

    except TypeError as e:
        logger.error(f"Ошибка при создании инлайн-клавиатуры: {e}")
        raise
    except ValueError as e:
        logger.error(f"Ошибка при создании инлайн-клавиатуры: {e}")
        raise
    except Exception as e:
        logger.error(f"Неизвестная ошибка при создании инлайн-клавиатуры: {e}")
        raise
