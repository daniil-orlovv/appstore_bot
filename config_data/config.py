from typing import Union

from dataclasses import dataclass
from environs import Env


@dataclass
class TgBot:
    token: str
    admin_ids: list[int]


@dataclass
class CheckingInterval:
    minutes: int = 1


@dataclass
class Config:
    tg_bot: TgBot
    interval_value: CheckingInterval

    def update_interval(self, new_value: int):
        self.interval_value.minutes = new_value


def load_config(path: Union[str, None] = None) -> Config:
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
