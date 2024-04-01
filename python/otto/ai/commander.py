from abc import ABC, abstractmethod

from otto.command import Command
from otto.context.window import WindowInfo


class Commander(ABC):
    @abstractmethod
    async def get_command(self, active_window: WindowInfo) -> Command:
        raise NotImplementedError
