from dataclasses import dataclass
from logging import Logger
from typing import Optional

from injector import inject
from pywinauto.win32_hooks import Hook, KeyboardEvent, MouseEvent
from pywinauto import Application
from pywinauto import Desktop
import time
import threading

from otto.context.window import WindowInfo


@inject
@dataclass
class OttoListener:
	_logger: Logger
	_hook: Optional[Hook] = None

	def listen(self):
		# TODO Maybe maybe it something more obscure like Shift+Esc?
		self._logger.info("Listening for events. Press Esc anytime with any window open to exit.")
		self._hook = Hook()
		self._hook.handler = self._keyboard_handler  # type: ignore

		# Start hook in a new thread so that it doesn't block.
		# Was `self._hook.hook(keyboard=True)`.
		# thread = threading.Thread(target=self._hook.hook, kwargs={'keyboard': True})
		# thread.start()

		while True:
			try:
				active_window = self._get_active_window_info()
			except Exception as e:
				self._logger.error("Error: %s", e)
				break

			time.sleep(1)

		# thread.join()

	def _get_active_window_info(self) -> Optional[WindowInfo]:
		desktop = Desktop(backend='uia')

		active_windows = desktop.windows(active_only=True)
		if not active_windows:
			# Doesn't find the window when the Start Menu or Task Manager is open.
			self._logger.debug("No active windows.")
			return None
		active_window = active_windows[0]
		assert active_window.is_active()
		window_title = active_window.window_text()
		self._logger.info("Active window title: \"%s\"", window_title)
		# TODO Get more information about the windows like text they're entering in input fields.
		# TODO Figure more ways to get input elements.
		input_elements = active_window.descendants(control_type='Edit')
		for i in input_elements:
			self._logger.info("Input element: %s", i)
		result = WindowInfo(
                    title=window_title
                )

		self._logger.debug("Active window: \"%s\"", result)

		# Alternative way, but there are multiple `window_text`s in Windows Explorer.
		# app = Application(backend='uia')
		# active_app = app.connect(active_only=True)
		# window = active_app.window()
		# assert window.is_active()

		return result

	def _keyboard_handler(self, event: KeyboardEvent | MouseEvent) -> None:
		assert isinstance(event, KeyboardEvent), \
			f"Only KeyboardEvent is supported at the moment. Got {type(event)} instead."
		# For extra help:
		# self._logger.debug("%s: %s", event.event_type, event.current_key)

		# Handle exiting.
		if event.current_key == 'Escape' and event.event_type == 'key down':
			self._logger.info("Exiting because '%s' was pressed", event.current_key)
			if self._hook is not None:
				# TODO Stop the listening loop too.
				self._hook.stop()
				self._hook = None
