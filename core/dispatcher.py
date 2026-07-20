from core.state_manager import StateManager
from core.module import ModuleResult


class Dispatcher:
    def __init__(self):
        print("[INFO] Dispatcher initialized")

        self.state_manager = StateManager()

        self.modules = []
        self.system_modules = []
        self.user_modules = []

        self.game_state = None


    def set_game_state(self, game_state):
        self.game_state = game_state


    def start(self):
        self.state_manager.set_state("READY")
        print("[INFO] System ready")


    def register_module(self, module):

        self.modules.append(module)

        if module.module_type == "system":
            self.system_modules.append(module)
        else:
            self.user_modules.append(module)


    def run_system_modules(self, context):

        for module in self.system_modules:

            if not module.enabled:
                continue

            result = module.run(context)

            if result != ModuleResult.SUCCESS:

                print(
                    f"[ERROR] System module failed: {module.name}"
                )

                return False

        return True


    def run_modules(self, context):

        for module in self.user_modules:
            if module.enabled:
                module.run(context)


    def run_cycle(self, character_manager, context, cycles=1):

        if not self.run_system_modules(context):
            return

        for _ in range(cycles):

            character = character_manager.get_next_character()

            if character is None:
                print("[ERROR] No characters found")
                return

            print(f"[CHARACTER] {character}")

            context.session.set_location(
                None,
                None,
                character
            )

            self.run_modules(context)