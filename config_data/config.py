from dataclasses import dataclass
from typing import Union

from environs import Env


@dataclass
class TgBot:
    """Класс для хранения токена от телеграм-бота и списка админов."""
    token: str
    admin_ids: list[int]


@dataclass
class CheckingInterval:
    """Класс для хранения значения, используемого для проверки доступа
    приложений."""
    minutes: int


@dataclass
class Config:
    """Родительский класс для классов токена и интервала."""
    tg_bot: TgBot
    interval_value: CheckingInterval

    def update_interval(self, new_value: int):
        """Метод класса, обновляющий значение интервала для проверки
        доступности приложений в минутах."""
        self.interval_value.minutes = new_value


def load_config(path: Union[str, None] = None) -> Config:
    """Функция для загрузки данных из файла окружения .env."""
    env = Env()
    env.read_env(path)
    return Config(
        tg_bot=TgBot(
            token=env('BOT_TOKEN'),
            admin_ids=list(map(int, env.list('ADMIN_IDS')))
        ),
        interval_value=CheckingInterval(
            minutes=env('INTERVAL_MINUTES')
        )
    )
