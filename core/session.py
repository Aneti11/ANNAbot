class Session:
    def __init__(self):
        self.current_account = None
        self.current_igg_id = None
        self.current_character = None

    def set_character(self, character):
        self.current_character = character

    def get_character(self):
        return self.current_character