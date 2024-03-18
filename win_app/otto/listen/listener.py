from dataclasses import dataclass
from logging import Logger
from typing import Optional

from injector import inject
from pywinauto.win32_hooks import Hook, KeyboardEvent, MouseEvent


@inject
@dataclass
class OttoListener:
	_logger: Logger
	_hook: Optional[Hook] = None

	def listen(self):
		# TODO Maybe maybe it something more obscure like Shift+Esc?
		self._logger.info("Listening for events. Presse Esc anytime with any window open to exit.")
		self._hook = Hook()
		self._hook.handler = self._keyboard_handler  # type: ignore
		self._hook.hook(keyboard=True)

	def _keyboard_handler(self, event: KeyboardEvent | MouseEvent) -> None:
		assert isinstance(event, KeyboardEvent), \
			f"Only KeyboardEvent is supported at the moment. Got {type(event)} instead."
		# For extra help:
		# self._logger.debug("%s: %s", event.event_type, event.current_key)

		# Handle exiting.
		if event.current_key == 'Escape' and event.event_type == 'key down':
			self._logger.info("Exiting because '%s' was pressed", event.current_key)
			if self._hook is not None:
				self._hook.stop()
				self._hook = None
