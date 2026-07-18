class Character:
    def __init__(self, character_id, nickname, enabled=True):
        self.character_id = character_id
        self.nickname = nickname
        self.enabled = enabled

    def __str__(self):
        return f"{self.nickname} ({self.character_id})"