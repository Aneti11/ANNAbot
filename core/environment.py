from adapters.emulator.ldplayer import LDPlayerAdapter
from core.config_loader import ConfigLoader
from pathlib import Path
from models.emulator_installation import EmulatorInstallation


class EnvironmentManager:
    """
    Управление рабочим окружением ANNAbot.

    Отвечает за:
    - проверку доступности окружения;
    - работу с эмулятором;
    - подготовку среды выполнения.
    """


    def __init__(self):

        self.connected = False

        self.emulator = LDPlayerAdapter()

        self.installation = None
        self.instance = None


    def check(self):
        """
        Проверка готовности окружения.
        """

        print("[ENV] Checking environment")

        settings = ConfigLoader.load_settings()

        saved_path = settings["environment"]["emulator"]["path"]

        installation = None

        if saved_path:
            path = Path(saved_path)

            if path.exists():
                print(
                    f"[ENV] Using saved LDPlayer path: {path}"
                )

                for console_name in ("ldconsole.exe", "dnconsole.exe"):
                    console = path / console_name

                    if console.exists():
                        installation = EmulatorInstallation(
                            path=path,
                            console=console,
                            executable=path / "dnplayer.exe",
                            source=settings["environment"]["emulator"].get(
                                "source",
                                "settings"
                            )
                        )
                        break

                if installation is None:
                    print(
                        "[ENV] Saved LDPlayer path is invalid, searching for installation"
                    )

        if installation is None:
            print("[ENV] Searching LDPlayer installation")
            installation = self.emulator.find_installation()

            if installation:
                settings["environment"]["emulator"]["path"] = (
                    str(installation.path)
                )

                settings["environment"]["emulator"]["source"] = (
                    installation.source
                )

                ConfigLoader.save_settings(
                    settings
                )

        self.installation = installation

        if self.installation:
            print(
                f"[ENV] LDPlayer found: "
                f"{self.installation.path}"
            )

            self.instance = self.emulator.find_instance(
                "ANNAbot"
            )

            if self.instance:
                print("[EMULATOR] Found instance: ANNAbot")
                print(f"[EMULATOR] Index: {self.instance.index}")
                print(f"[EMULATOR] Running: {self.instance.running}")
                print("[STATE] Environment detected")
                return True

            print("[ERROR] ANNAbot instance not found")
            return False

        print("[ENV] LDPlayer not found")

        return False


    def start(self):
        """
        Запуск окружения.
        """

        print("[ENV] Starting environment")

        return True


    def connect(self):
        """
        Подключение к окружению.
        """

        print("[ENV] Connecting environment")

        self.connected = True

        return True