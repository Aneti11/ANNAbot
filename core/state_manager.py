class StateManager:
    def __init__(self):
        self.state = "STARTING"

    def set_state(self, new_state):
        self.state = new_state
        print(f"[STATE] {self.state}")

    def get_state(self):
        return self.state