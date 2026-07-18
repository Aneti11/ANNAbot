from models.igg_account import IGGAccount
from models.igg_id import IGGID
from models.character import Character


account = IGGAccount("test@mail.com")

igg = IGGID(123456)

igg.add_character(
    Character(111, "Milamoria")
)

igg.add_character(
    Character(222, "Farm1", False)
)

account.add_igg_id(igg)


for character in account.get_enabled_characters():
    print(character)