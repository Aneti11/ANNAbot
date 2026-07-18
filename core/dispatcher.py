from core.state_manager import StateManager


class Dispatcher:
    def __init__(self):
        print("[INFO] Dispatcher initialized")

        self.state_manager = StateManager()
        self.modules = []


    def start(self):
        self.state_manager.set_state("READY")
        print("[INFO] System ready")


    def register_module(self, module):
        self.modules.append(module)


    def run_modules(self, session):
        for module in self.modules:
            module.run(session)


    def run_cycle(self, character_manager, session, cycles=1):
        for _ in range(cycles):

            character = character_manager.get_next_character()

            if character is None:
                print("[ERROR] No characters found")
                return

            print(f"[CHARACTER] {character}")

            session.set_location(
                None,
                None,
                character
            )

            self.run_modules(session)