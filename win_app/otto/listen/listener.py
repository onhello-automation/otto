from dataclasses import dataclass
from logging import Logger

from injector import inject


@inject
@dataclass
class OttoListener:
	_logger: Logger

	def listen(self):
		self._logger.info("Listening for events")
