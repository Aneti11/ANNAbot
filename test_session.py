from core.session import Session
from models.character import Character


session = Session()

character = Character(111, "Milamoria")

session.set_character(character)

current = session.get_character()

print(current)