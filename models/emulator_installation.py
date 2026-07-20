from pathlib import Path


class EmulatorInstallation:
    """
    Информация об установленном эмуляторе.
    """

    def __init__(
        self,
        path: Path,
        console: Path,
        executable: Path,
        version: str | None = None,
        source: str = "unknown"
    ):
        self.path = path
        self.console = console
        self.executable = executable
        self.version = version
        self.source = source


    def __str__(self):
        return str(self.path)