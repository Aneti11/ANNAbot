from core.dispatcher import Dispatcher
from core.session import Session
from core.character_manager import CharacterManager
from core.config_loader import ConfigLoader
from core.module_loader import ModuleLoader
from core.game_state import GameState
from core.context import ExecutionContext
from core.game import Game
from core.environment import EnvironmentManager
from core.logger import Logger


class Application:

    def __init__(self):
        self.dispatcher = Dispatcher()
        self.session = Session()
        self.game_state = GameState()
        self.game = Game()
        self.environment = EnvironmentManager()

        self.context = None

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

        if not self.environment.check():
            Logger.error("Environment not ready")
            return

        self.context = ExecutionContext(
            self.session,
            self.game_state,
            self.dispatcher.state_manager,
            self.game,
            self.environment
        )

        self.dispatcher.start()


    def run(self, cycles=5):

        self.dispatcher.run_cycle(
            self.character_manager,
            self.context,
            cycles
        )