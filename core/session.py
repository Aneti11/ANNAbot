class Session:
    def __init__(self):
        self.current_account = None
        self.current_igg_id = None
        self.current_character = None

    def set_location(self, account, igg_id, character):
        self.current_account = account
        self.current_igg_id = igg_id
        self.current_character = character

    def get_location(self):
        return (
            self.current_account,
            self.current_igg_id,
            self.current_character
        )