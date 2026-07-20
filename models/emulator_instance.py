class EmulatorInstance:
    """
    Экземпляр эмулятора LDPlayer.
    """

    def __init__(
        self,
        index: int,
        name: str,
        running: bool = False
    ):
        self.index = index
        self.name = name
        self.running = running


    def __str__(self):
        return f"{self.name} ({self.index})"