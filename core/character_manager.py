class CharacterManager:
    def __init__(self, accounts):
        self.accounts = accounts

        self.current_index = -1
        self.characters = []

        self._build_character_list()

    def _build_character_list(self):
        for account in self.accounts:
            for igg_id in account.igg_ids:
                for character in igg_id.characters:
                    if character.enabled:
                        self.characters.append(
                            character
                        )

    def get_next_character(self):
        if not self.characters:
            return None

        self.current_index += 1

        if self.current_index >= len(self.characters):
            self.current_index = 0

        return self.characters[self.current_index]