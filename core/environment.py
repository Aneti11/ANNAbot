from adapters.emulator.ldplayer import LDPlayerAdapter
from core.config_loader import ConfigLoader
from pathlib import Path


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


    def check(self):
        """
        Проверка готовности окружения.
        """

        print("[ENV] Checking environment")

        settings = ConfigLoader.load_settings()

        saved_path = settings["environment"]["emulator"]["path"]


        if saved_path:

            path = Path(saved_path)

            if path.exists():

                print(
                    f"[ENV] LDPlayer from settings: {path}"
                )

                return True


        self.installation = (
            self.emulator.find_installation()
        )


        if self.installation:

            print(
                f"[ENV] LDPlayer found: "
                f"{self.installation.path}"
            )


            settings["environment"]["emulator"]["path"] = (
                str(self.installation.path)
            )

            settings["environment"]["emulator"]["source"] = (
                self.installation.source
            )


            ConfigLoader.save_settings(
                settings
            )


            return True


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