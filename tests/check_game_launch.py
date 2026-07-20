import sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
if str(root) not in sys.path:
    sys.path.insert(0, str(root))

from core.config_loader import ConfigLoader
from core.environment import EnvironmentManager
from core.game_launcher import GameLauncher
from adapters.emulator.ldplayer import LDPlayerAdapter
from adapters.android.adb import ADBAdapter


def main():
    settings = ConfigLoader.load_settings()

    env = EnvironmentManager()
    env.emulator = LDPlayerAdapter()

    installation = env.emulator.find_installation()
    if installation is None:
        print("ERROR: LDPlayer installation not found")
        return

    env.installation = installation

    instance = env.emulator.find_instance("ANNAbot")
    if instance is None:
        print("ERROR: ANNAbot instance not found")
        return

    env.instance = instance
    env.adb = ADBAdapter(installation)
    env.game_package = settings["environment"].get("package_name", "").strip()

    print(f"Selected instance: {env.instance.name} (index={env.instance.index}, running={env.instance.running})")
    print(f"Configured package_name: '{env.game_package}'")

    launcher = GameLauncher(
        env.installation,
        env.instance,
        env.game_package
    )

    result = launcher.launch()
    print(f"launch_game result: {result}")


if __name__ == "__main__":
    main()
