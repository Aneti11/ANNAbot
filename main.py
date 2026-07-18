from core.dispatcher import Dispatcher
from core.session import Session
from core.character_manager import CharacterManager

from models.igg_account import IGGAccount
from models.igg_id import IGGID
from models.character import Character

from modules.m00_test import TestModule


# Создаем тестовую структуру аккаунтов

account = IGGAccount(
    "test@mail.com"
)

igg = IGGID(
    123456
)

igg.add_character(
    Character(
        111,
        "Milamoria"
    )
)

igg.add_character(
    Character(
        222,
        "Farm1"
    )
)

account.add_igg_id(
    igg
)


# Создаем менеджеры

character_manager = CharacterManager(
    [account]
)

session = Session()


# Создаем приложение

app = Dispatcher()

app.register_module(
    TestModule()
)


app.start()


# Запускаем цикл

app.run_cycle(
    character_manager,
    session,
    cycles=5
)