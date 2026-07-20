from pathlib import Path
import logging


class Logger:
    """Unified ANNAbot logger wrapper around standard Python logging."""

    _logger = None

    @classmethod
    def _ensure_logger(cls):
        if cls._logger is None:
            cls._logger = logging.getLogger("annabot")
            cls._logger.setLevel(logging.DEBUG)

            if not cls._logger.handlers:
                formatter = logging.Formatter(
                    "%(asctime)s [%(levelname)s] %(message)s",
                    "%Y-%m-%d %H:%M:%S"
                )

                console_handler = logging.StreamHandler()
                console_handler.setFormatter(formatter)
                cls._logger.addHandler(console_handler)

                logs_dir = Path(__file__).resolve().parents[1] / "logs"
                logs_dir.mkdir(parents=True, exist_ok=True)

                file_handler = logging.FileHandler(
                    logs_dir / "annabot.log",
                    encoding="utf-8"
                )
                file_handler.setFormatter(formatter)
                cls._logger.addHandler(file_handler)

        return cls._logger

    @classmethod
    def info(cls, message):
        cls._ensure_logger().info(message)

    @classmethod
    def warning(cls, message):
        cls._ensure_logger().warning(message)

    @classmethod
    def error(cls, message):
        cls._ensure_logger().error(message)

    @classmethod
    def debug(cls, message):
        cls._ensure_logger().debug(message)
