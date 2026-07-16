from core.state_manager import StateManager


class Dispatcher:
    def __init__(self):
        print("[INFO] Dispatcher initialized")
        self.state_manager = StateManager()

    def start(self):
        self.state_manager.set_state("READY")
        print("[INFO] System ready")