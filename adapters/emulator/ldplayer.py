import subprocess
import time
from pathlib import Path

from models.emulator_installation import EmulatorInstallation
from models.emulator_instance import EmulatorInstance
from core.logger import Logger
from core.platform.registry import (
    WindowsRegistry,
    CURRENT_USER,
    LOCAL_MACHINE
)


class LDPlayerAdapter:
    """
    Адаптер для работы с LDPlayer.
    """

    REGISTRY_PATHS = [
        (
            CURRENT_USER,
            r"Software\XuanZhi\LDPlayer9"
        ),
        (
            LOCAL_MACHINE,
            r"SOFTWARE\XuanZhi\LDPlayer9"
        )
    ]


    def find_installation(self):

        for root, key in self.REGISTRY_PATHS:

            install_dir = WindowsRegistry.get_value(
                root,
                key,
                "InstallDir"
            )

            if install_dir:

                path = Path(install_dir)

                for console_name in ("ldconsole.exe", "dnconsole.exe"):
                    console = path / console_name

                    if console.exists():
                        return EmulatorInstallation(
                            path=path,
                            console=console,
                            executable=path / "dnplayer.exe",
                            source="registry"
                        )

        return None


    def find_instance(self, name: str):
        installation = self.find_installation()

        if installation is None:
            return None

        console_path = installation.console

        try:
            result = subprocess.run(
                [str(console_path), "list2"],
                capture_output=True,
                text=True,
                check=True
            )
        except (subprocess.CalledProcessError, FileNotFoundError):
            return None

        running_instance = None

        for line in result.stdout.splitlines():
            line = line.strip()

            if not line:
                continue

            parts = line.split(",")

            if len(parts) < 5:
                continue

            instance_index = parts[0].strip()
            instance_name = parts[1].strip()
            android_state = parts[4].strip()

            Logger.debug(f"[LDPLAYER] list2 line: {parts}")

            try:
                index = int(instance_index)
            except ValueError:
                continue

            if android_state == "1":
                state = EmulatorInstance.RUNNING
            elif android_state == "2":
                state = EmulatorInstance.STARTING
            else:
                state = EmulatorInstance.STOPPED

            if instance_name == name:
                return EmulatorInstance(
                    index=index,
                    name=instance_name,
                    state=state
                )

            if name.lower() in instance_name.lower():
                return EmulatorInstance(
                    index=index,
                    name=instance_name,
                    state=state
                )

            if state == EmulatorInstance.RUNNING and running_instance is None:
                running_instance = EmulatorInstance(
                    index=index,
                    name=instance_name,
                    state=state
                )

        if running_instance is not None:
            Logger.warning(
                f"[LDPLAYER] Instance '{name}' not found; falling back to running instance '{running_instance.name}'"
            )
            return running_instance

        return None


    def start_instance(self, index: int):
        installation = self.find_installation()

        if installation is None:
            return False

        command = [
            str(installation.console),
            "launch",
            "--index",
            str(index)
        ]

        try:
            subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=True
            )
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False


    def wait_until_ready(self, index: int, timeout: int = 60):
        deadline = time.time() + timeout

        while time.time() < deadline:
            installation = self.find_installation()
            if installation is None:
                return False

            try:
                result = subprocess.run(
                    [str(installation.console), "list2"],
                    capture_output=True,
                    text=True,
                    check=True
                )
            except (subprocess.CalledProcessError, FileNotFoundError):
                return False

            for line in result.stdout.splitlines():
                line = line.strip()

                if not line:
                    continue

                parts = line.split(",")

                if len(parts) < 5:
                    continue

                try:
                    instance_index = int(parts[0].strip())
                except ValueError:
                    continue

                if instance_index != index:
                    continue

                android_state = parts[4].strip()
                if android_state == "1":
                    return True
                if android_state == "2":
                    break

            time.sleep(2)

        return False