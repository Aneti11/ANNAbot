from adapters.android.adb import ADBAdapter
from core.logger import Logger


class GameLauncher:
    """Handles Android game launch via LDPlayer ADB."""

    def __init__(self, installation, instance, package_name=None):
        self.installation = installation
        self.instance = instance
        self.package_name = package_name
        self.adb = ADBAdapter(installation) if installation is not None else None

    def launch(self, package_name=None):
        if self.installation is None or self.instance is None:
            Logger.error("[ADB] No emulator instance available for game launch")
            return False

        if self.adb is None:
            self.adb = ADBAdapter(self.installation)

        package = package_name or self.package_name

        if not package:
            Logger.error(
                "[ADB] No Android package name configured for game launch"
            )
            return False

        Logger.info(f"[ADB] Launching game package: {package}")

        result = self.adb.run_app(self.instance.index, package)

        if result is None or result.returncode != 0:
            stderr = result.stderr.strip() if result is not None else ""
            Logger.error(
                f"[ADB] Failed to launch {package}. "
                f"{stderr}"
            )
            return False

        Logger.info("[ADB] Launch request issued successfully")
        return True
