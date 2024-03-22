from dataclasses import dataclass
from logging import Logger
from typing import Optional

from injector import inject
from pywinauto.win32_hooks import Hook, KeyboardEvent, MouseEvent
from pywinauto import Application
from pywinauto import Desktop
import time

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

		# Start a new thread.
		# self._hook.hook(keyboard=True)

		while True:
			print("*******************")

			# Get the active window
			desktop = Desktop(backend='uia')

			active_windows = desktop.windows(active_only=True)
			if not active_windows:
				# Doesn't find the window when the Start Menu or Task Manager is open.
				print("No active windows.")
				time.sleep(1)
				continue
			active_window = active_windows[0]
			print("Active Window:")
			print(active_window.window_text())
			assert active_window.is_active()
			
			# Alternative way, but there are multiple `window_text`s in Windows Explorer.
			# app = Application(backend='uia')
			# active_app = app.connect(active_only=True)
			# window = active_app.window()
			# assert window.is_active()


			time.sleep(1)

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
