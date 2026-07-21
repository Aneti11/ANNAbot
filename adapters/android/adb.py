import subprocess
import time
from pathlib import Path

from core.logger import Logger
from models.emulator_installation import EmulatorInstallation


class ADBAdapter:
    """ADB adapter for LDPlayer Android device management."""

    def __init__(self, installation: EmulatorInstallation):
        self.installation = installation

    def _run_ldconsole_adb(self, index: int, command: str, timeout: int = 30):
        cmd = [
            str(self.installation.console),
            "adb",
            "--index",
            str(index),
            "--command",
            command
        ]

        Logger.debug(f"[ADB] Running: {cmd}")

        try:
            return subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout
            )
        except FileNotFoundError:
            Logger.error("[ADB] ldconsole executable not found")
            return None
        except subprocess.SubprocessError as exc:
            Logger.error(f"[ADB] subprocess failed: {exc}")
            return None

    def get_devices(self, index: int):
        result = self._run_ldconsole_adb(index, "devices", timeout=15)

        if result is None or result.returncode != 0:
            return []

        devices = []

        for line in result.stdout.splitlines():
            line = line.strip()

            if not line or line.startswith("List of devices attached"):
                continue

            parts = line.split()

            if len(parts) < 2:
                continue

            devices.append({
                "serial": parts[0],
                "state": parts[1]
            })

        return devices

    def is_device_online(self, index: int):
        return any(
            device["state"] == "device"
            for device in self.get_devices(index)
        )

    def is_available(self, index: int):
        devices = self.get_devices(index)

        if not devices:
            Logger.warning(
                f"[ADB] No devices found for index {index}. "
                "ADB layer is unavailable."
            )
            return False

        if self.is_device_online(index):
            return True

        Logger.warning(
            f"[ADB] Device(s) attached but not online for index {index}: {devices}"
        )
        return False

    def shell_command(self, index: int, args: list[str], timeout: int = 30):
        command = "shell " + " ".join(args)
        return self._run_ldconsole_adb(index, command, timeout=timeout)

    def run_app(self, index: int, package_name: str, timeout: int = 30):
        cmd = [
            str(self.installation.console),
            "runapp",
            "--index",
            str(index),
            "--packagename",
            package_name
        ]

        Logger.debug(f"[ADB] Running app: {cmd}")

        try:
            return subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout
            )
        except FileNotFoundError:
            Logger.error("[ADB] ldconsole executable not found")
            return None
        except subprocess.SubprocessError as exc:
            Logger.error(f"[ADB] subprocess failed: {exc}")
            return None

    def wait_until_ready(self, index: int, timeout: int = 120):
        deadline = time.time() + timeout

        while time.time() < deadline:
            devices = self.get_devices(index)

            online_device = next(
                (device for device in devices if device["state"] == "device"),
                None
            )

            if online_device is None:
                Logger.debug(
                    f"[ADB] Waiting for device {index} to appear. "
                    f"Current devices: {devices}"
                )
                time.sleep(2)
                continue

            response = self.shell_command(
                index,
                ["getprop", "sys.boot_completed"],
                timeout=10
            )

            if response is None or response.returncode != 0:
                Logger.debug(
                    f"[ADB] Failed to read boot status for device {index}. "
                    "Retrying until timeout."
                )
                time.sleep(2)
                continue

            if response.stdout.strip() == "1":
                Logger.info(f"[ADB] Device {index} booted")
                return True

            Logger.debug(
                f"[ADB] Device {index} is online but boot not complete: "
                f"{response.stdout.strip()}"
            )
            time.sleep(2)

        Logger.error(
            f"[ADB] Timeout waiting for device {index} to become ready "
            f"after {timeout} seconds."
        )
        return False
