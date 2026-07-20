class EmulatorInstance:
    """
    Экземпляр эмулятора LDPlayer.
    """

    STOPPED = "STOPPED"
    STARTING = "STARTING"
    RUNNING = "RUNNING"

    def __init__(
        self,
        index: int,
        name: str,
        state: str = STOPPED
    ):
        self.index = index
        self.name = name
        self.state = state

    @property
    def running(self):
        return self.state == self.RUNNING

    def __str__(self):
        return f"{self.name} ({self.index})"
