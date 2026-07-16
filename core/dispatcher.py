from core.state_manager import StateManager
from core.module import ModuleResult


class Dispatcher:
    def __init__(self):
        print("[INFO] Dispatcher initialized")

        self.state_manager = StateManager()
        self.modules = []

    def register_module(self, module):
        """
        Добавляет модуль в список выполнения.
        """
        self.modules.append(module)

    def run_modules(self):
        """
        Выполняет все зарегистрированные модули по порядку.
        """

        for module in self.modules:
            print(f"[MODULE] Starting: {module.name}")

            if not module.can_run(self.state_manager):
                print(f"[MODULE] Skipped: {module.name}")
                continue

            result = module.run(self.state_manager)

            print(
                f"[MODULE] Finished: {module.name} -> {result.value}"
            )

            if result == ModuleResult.FAILED:
                print("[ERROR] Module failed")
                break

    def start(self):
        self.state_manager.set_state("READY")
        print("[INFO] System ready")