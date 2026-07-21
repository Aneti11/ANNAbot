import ctypes
import os
import platform
from pathlib import Path
from typing import Optional

from adapters.android.adb import ADBAdapter
from adapters.emulator.ldplayer import LDPlayerAdapter
from core.logger import Logger
from models.emulator_installation import EmulatorInstallation
from models.emulator_instance import EmulatorInstance


class ValidationResult:
    def __init__(self, valid: bool, issues: list[str]):
        self.valid = valid
        self.issues = issues


class EnvironmentValidator:
    """Validates LDPlayer instance and host environment for ANNAbot."""

    def __init__(
        self,
        installation: Optional[EmulatorInstallation],
        instance: Optional[EmulatorInstance],
        adb_adapter: Optional[ADBAdapter] = None,
        emulator_adapter: Optional[LDPlayerAdapter] = None
    ):
        self.installation = installation
        self.instance = instance
        self.adb_adapter = adb_adapter
        self.emulator_adapter = emulator_adapter or LDPlayerAdapter()

    def validate_settings(self) -> ValidationResult:
        issues: list[str] = []

        if self.installation is None or self.instance is None:
            issues.append(
                "[ERROR] Environment:\nMissing LDPlayer installation or instance information"
            )
            self._log_result(issues)
            return ValidationResult(False, issues)

        instance_config = self._get_instance_config()

        if instance_config is None:
            issues.append(
                "[ERROR] Environment:\nUnable to read LDPlayer instance configuration"
            )
        else:
            self._validate_name(instance_config, issues)
            self._validate_resolution(instance_config, issues)
            self._validate_dpi(instance_config, issues)
            self._validate_adb_setting(instance_config, issues)

        self._validate_cpu(issues)
        self._validate_ram(issues)

        self._log_result(issues)
        return ValidationResult(not issues, issues)

    def validate_runtime(self) -> ValidationResult:
        issues: list[str] = []

        if self.installation is None or self.instance is None:
            issues.append(
                "[ERROR] Environment:\nMissing LDPlayer installation or instance information"
            )
            self._log_result(issues)
            return ValidationResult(False, issues)

        self._validate_adb(issues)
        self._log_result(issues)
        return ValidationResult(not issues, issues)

    def _validate_name(self, config: dict, issues: list[str]):
        player_name = config.get("playerName")

        if player_name != "ANNAbot":
            issues.append(
                "[ERROR] Player name:\n"
                f"Current: {player_name}\n"
                "Required: ANNAbot"
            )

    def _validate_resolution(self, config: dict, issues: list[str]):
        width = config.get("width")
        height = config.get("height")

        if width != 800 or height != 450:
            issues.append(
                "[ERROR] Wrong resolution. "
                f"Required 800x450, current {width}x{height}"
            )

    def _validate_dpi(self, config: dict, issues: list[str]):
        dpi = config.get("dpi")

        if dpi != 160:
            issues.append(
                "[ERROR] Wrong DPI. "
                f"Required 160, current {dpi}"
            )

    def _validate_adb_setting(self, config: dict, issues: list[str]):
        adb_debug = config.get("adbDebug")
        if adb_debug == 1:
            return

        if adb_debug == 0:
            issues.append(
                "[ERROR] ADB disabled. Enable Local connection in LDPlayer settings"
            )
            return

        if adb_debug == 2:
            issues.append(
                "[ERROR] Remote ADB is not supported. Enable Local connection in LDPlayer settings"
            )
            return

        # Treat unknown/absent values as disabled
        issues.append(
            "[ERROR] ADB disabled. Enable Local connection in LDPlayer settings"
        )

    def _validate_cpu(self, issues: list[str]):
        cpu_count = os.cpu_count() or 1

        if cpu_count < 2:
            issues.append(
                "[ERROR] CPU:\n"
                f"Current: {cpu_count}\n"
                "Required: 2"
            )

    def _validate_ram(self, issues: list[str]):
        ram_mb = self._get_total_memory_mb()

        if ram_mb is None:
            Logger.warning("[VALIDATOR] Unable to determine total system memory")
            return

        if ram_mb < 3072:
            issues.append(
                "[ERROR] RAM:\n"
                f"Current: {ram_mb} MB\n"
                "Required: 3072 MB"
            )

    def _validate_adb(self, issues: list[str]):
        if self.adb_adapter is None:
            if self.installation is None:
                issues.append(
                    "[ERROR] ADB:\nUnable to initialize ADB adapter"
                )
                return

            self.adb_adapter = ADBAdapter(self.installation)

        devices = self.adb_adapter.get_devices(self.instance.index)

        if not devices:
            issues.append(
                "[ERROR] ADB:\nDisabled or no devices found via ldconsole adb"
            )
            return

        online = any(
            device["state"] == "device"
            for device in devices
        )

        if not online:
            issues.append(
                "[ERROR] ADB:\nNo online device available for index "
                f"{self.instance.index}"
            )

    def _get_instance_config(self) -> Optional[dict]:
        if self.installation is None:
            return None

        config = self.emulator_adapter.get_instance_config(
            self.installation,
            self.instance.index
        )

        return config

    def _get_total_memory_mb(self) -> Optional[int]:
        system = platform.system()

        if system == "Windows":
            try:
                class MEMORYSTATUSEX(ctypes.Structure):
                    _fields_ = [
                        ("dwLength", ctypes.c_ulong),
                        ("dwMemoryLoad", ctypes.c_ulong),
                        ("ullTotalPhys", ctypes.c_ulonglong),
                        ("ullAvailPhys", ctypes.c_ulonglong),
                        ("ullTotalPageFile", ctypes.c_ulonglong),
                        ("ullAvailPageFile", ctypes.c_ulonglong),
                        ("ullTotalVirtual", ctypes.c_ulonglong),
                        ("ullAvailVirtual", ctypes.c_ulonglong),
                        ("ullAvailExtendedVirtual", ctypes.c_ulonglong),
                    ]

                stat = MEMORYSTATUSEX()
                stat.dwLength = ctypes.sizeof(stat)
                if ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(stat)):
                    return int(stat.ullTotalPhys // (1024 * 1024))
            except Exception:
                return None

        if hasattr(os, "sysconf"):
            try:
                pages = os.sysconf("SC_PHYS_PAGES")
                page_size = os.sysconf("SC_PAGE_SIZE")
                return int((pages * page_size) // (1024 * 1024))
            except (ValueError, OSError, AttributeError):
                return None

        return None

    def validate(self) -> ValidationResult:
        return self.validate_runtime()

    def _log_result(self, issues: list[str]):
        if not issues:
            Logger.info("Environment validation passed")
            return

        Logger.error("Environment validation failed")

        for issue in issues:
            Logger.error(issue)
