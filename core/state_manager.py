class StateManager:
    def __init__(self):
        self.system_state = "STARTING"

        self.data = {
            "account": None,
            "current_module": None,
            "window": None
        }

    def set_state(self, new_state):
        self.system_state = new_state
        print(f"[STATE] {self.system_state}")

    def get_state(self):
        return self.system_state

    def set_data(self, key, value):
        self.data[key] = value

    def get_data(self, key):
        return self.data.get(key)