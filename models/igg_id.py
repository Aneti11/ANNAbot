class IGGID:
    def __init__(self, igg_id):
        self.igg_id = igg_id
        self.characters = []

    def add_character(self, character):
        self.characters.append(character)

    def get_enabled_characters(self):
        return [
            character
            for character in self.characters
            if character.enabled
        ]