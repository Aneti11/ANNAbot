from adapters.emulator.ldplayer import LDPlayerAdapter


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

        self.installation = (
            self.emulator.find_installation()
        )

        if self.installation:

            print(
                f"[ENV] LDPlayer found: "
                f"{self.installation.path}"
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