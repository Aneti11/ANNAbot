from adapters.emulator.ldplayer import LDPlayerAdapter
from core.config_loader import ConfigLoader
from core.logger import Logger
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

        Logger.info("[ENV] Checking environment")

        settings = ConfigLoader.load_settings()

        saved_path = settings["environment"]["emulator"]["path"]

        installation = None

        if saved_path:
            path = Path(saved_path)

            if path.exists():
                Logger.info(
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
                    Logger.warning(
                        "[ENV] Saved LDPlayer path is invalid, searching for installation"
                    )

        if installation is None:
            Logger.info("[ENV] Searching LDPlayer installation")
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
            Logger.info(
                f"[ENV] LDPlayer found: "
                f"{self.installation.path}"
            )

            self.instance = self.emulator.find_instance(
                "ANNAbot"
            )

            if self.instance:
                Logger.info("[EMULATOR] Found instance: ANNAbot")
                Logger.info(f"[EMULATOR] Index: {self.instance.index}")
                Logger.info(f"[EMULATOR] Running: {self.instance.running}")

                if self.instance.running:
                    Logger.info("[STATE] Environment detected")
                    return True

                Logger.info("[EMULATOR] Starting...")
                if not self.emulator.start_instance(self.instance.index):
                    Logger.error("[ERROR] Failed to start ANNAbot instance")
                    return False

                Logger.info("[EMULATOR] Waiting for startup...")
                if self.emulator.wait_until_ready(self.instance.index):
                    Logger.info("[EMULATOR] Ready")
                    Logger.info("[STATE] Environment detected")
                    return True

                Logger.error("[ERROR] ANNAbot instance did not become ready")
                return False

            Logger.error("[ERROR] ANNAbot instance not found")
            return False

        Logger.error("[ENV] LDPlayer not found")

        return False


    def start(self):
        """
        Запуск окружения.
        """

        Logger.info("[ENV] Starting environment")

        return True


    def connect(self):
        """
        Подключение к окружению.
        """

        Logger.info("[ENV] Connecting environment")

        self.connected = True

        return True