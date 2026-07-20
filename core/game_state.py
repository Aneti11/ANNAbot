class GameState:

    def __init__(self):
        self.window = None
        self.screen = None
        self.ready = False

    def set_window(self, window):
        self.window = window

    def get_window(self):
        return self.window

    def set_ready(self, value):
        self.ready = value

    def is_ready(self):
        return self.ready