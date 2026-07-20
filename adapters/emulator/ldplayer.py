from pathlib import Path

from models.emulator_installation import EmulatorInstallation
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

                console = path / "dnconsole.exe"

                if console.exists():

                    return EmulatorInstallation(
                        path=path,
                        console=console,
                        executable=path / "dnplayer.exe",
                        source="registry"
                    )

        return None