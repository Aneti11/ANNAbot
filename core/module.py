from abc import ABC, abstractmethod
from enum import Enum


class ModuleResult(Enum):
    SUCCESS = "success"
    FAILED = "failed"
    SKIPPED = "skipped"


class Module(ABC):
    """
    Базовый класс для всех модулей ANNAbot.
    """

    def __init__(self, name):
        self.name = name
        self.enabled = True

    def can_run(self, state):
        """
        Проверка, нужно ли выполнять модуль.
        """
        return self.enabled

    @abstractmethod
    def run(self, state):
        """
        Основное действие модуля.
        """
        pass