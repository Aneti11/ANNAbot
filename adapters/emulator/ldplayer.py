import subprocess
from pathlib import Path

from models.emulator_installation import EmulatorInstallation
from models.emulator_instance import EmulatorInstance
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

        for line in result.stdout.splitlines():
            line = line.strip()

            if not line:
                continue

            parts = line.split(",")

            if len(parts) < 3:
                continue

            instance_index = parts[0].strip()
            instance_name = parts[1].strip()
            running_flag = parts[2].strip()

            if instance_name == name:
                try:
                    index = int(instance_index)
                except ValueError:
                    continue

                running = running_flag != "0"

                return EmulatorInstance(
                    index=index,
                    name=instance_name,
                    running=running
                )

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