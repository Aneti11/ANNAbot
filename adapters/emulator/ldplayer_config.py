import json
from pathlib import Path
from typing import Any, Optional

from core.logger import Logger
from models.emulator_installation import EmulatorInstallation


class LDPlayerConfigReader:
    """Reads LDPlayer instance configuration from leidian*.config."""

    @staticmethod
    def read_instance_config(
        installation: EmulatorInstallation,
        index: int
    ) -> Optional[dict]:
        config_path = installation.path / "vms" / "config" / f"leidian{index}.config"

        Logger.debug("[LDPLAYER CONFIG] Looking for config:")
        Logger.debug(str(config_path))
        exists = config_path.exists()
        Logger.debug(f"[LDPLAYER CONFIG] Exists: {exists}")

        if not exists:
            Logger.error(f"[LDPLAYER] Config file not found: {config_path}")
            return None

        try:
            text = config_path.read_text(encoding="utf-8", errors="ignore")
            Logger.debug("[LDPLAYER CONFIG] Opened: True")
        except OSError as exc:
            Logger.error(
                f"[LDPLAYER] Failed to read LDPlayer config file {config_path}: {exc}"
            )
            return None

        raw_config = LDPlayerConfigReader._parse_config_text(text)

        if raw_config is None:
            return None

        Logger.debug(f"[LDPLAYER CONFIG] Loaded keys: {len(raw_config.keys())}")

        return {
            "playerName": LDPlayerConfigReader._get_nested(
                raw_config, "statusSettings.playerName"
            ),
            "adbDebug": LDPlayerConfigReader._get_nested(
                raw_config, "basicSettings.adbDebug"
            ),
            "width": LDPlayerConfigReader._get_nested(
                raw_config, "advancedSettings.resolution.width"
            ),
            "height": LDPlayerConfigReader._get_nested(
                raw_config, "advancedSettings.resolution.height"
            ),
            "dpi": LDPlayerConfigReader._get_nested(
                raw_config, "advancedSettings.resolutionDpi"
            ),
            "cpuCount": LDPlayerConfigReader._get_nested(
                raw_config, "advancedSettings.cpuCount"
            ),
            "memorySize": LDPlayerConfigReader._get_nested(
                raw_config, "advancedSettings.memorySize"
            ),
        }

    @staticmethod
    def _parse_config_text(text: str) -> Optional[dict]:
        try:
            parsed = json.loads(text)
        except json.JSONDecodeError:
            return LDPlayerConfigReader._parse_key_value(text)

        if not isinstance(parsed, dict):
            return None

        config: dict[str, Any] = {}

        for key, value in parsed.items():
            LDPlayerConfigReader._set_nested(config, key, value)

        return config

    @staticmethod
    def _parse_key_value(text: str) -> dict:
        config: dict[str, Any] = {}

        for raw_line in text.splitlines():
            line = raw_line.strip()

            if not line or line.startswith("#") or line.startswith(";"):
                continue

            if "=" not in line:
                continue

            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")

            if value.isdigit():
                parsed_value: Any = int(value)
            else:
                try:
                    float_value = float(value)
                    parsed_value = int(float_value) if float_value.is_integer() else float_value
                except ValueError:
                    parsed_value = value

            LDPlayerConfigReader._set_nested(config, key, parsed_value)

        return config

    @staticmethod
    def _set_nested(config: dict[str, Any], key: str, value: Any):
        parts = key.split(".")
        current = config

        for part in parts[:-1]:
            if part not in current or not isinstance(current[part], dict):
                current[part] = {}
            current = current[part]

        current[parts[-1]] = value

    @staticmethod
    def _get_nested(config: dict[str, Any], dotted_key: str) -> Any:
        current: Any = config

        for part in dotted_key.split("."):
            if not isinstance(current, dict) or part not in current:
                return None
            current = current[part]

        return current
