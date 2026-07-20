class ExecutionContext:

    def __init__(
        self,
        session,
        game_state,
        state_manager,
        game,
        environment
    ):
        self.session = session
        self.game_state = game_state
        self.state_manager = state_manager
        self.game = game
        self.environment = environment