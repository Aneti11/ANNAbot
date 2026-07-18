from core.dispatcher import Dispatcher
from core.session import Session
from core.character_manager import CharacterManager
from core.config_loader import ConfigLoader
from core.module_loader import ModuleLoader


class Application:

    def __init__(self):
        self.dispatcher = Dispatcher()
        self.session = Session()

        self.character_manager = None


    def setup(self):

        accounts = ConfigLoader.load_accounts()

        self.character_manager = CharacterManager(
            accounts
        )

        modules = ModuleLoader.load_modules()

        for module in modules:
            self.dispatcher.register_module(
                module
            )


    def start(self):

        self.setup()

        self.dispatcher.start()


    def run(self, cycles=5):

        self.dispatcher.run_cycle(
            self.character_manager,
            self.session,
            cycles
        )