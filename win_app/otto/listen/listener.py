from dataclasses import dataclass
from logging import Logger
from typing import Optional
from psutil import Process

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
                if active_window is not None:
                    # TODO
                    pass
            except Exception as e:
                self._logger.error("Error: %s", e)
                break

            time.sleep(1)

        # thread.join()

    def _get_active_window_info(self) -> Optional[WindowInfo]:
        desktop = Desktop(backend='uia')

        active_window = desktop.window(active_only=True)
        if not active_window.exists():
            # This can happen when the Start Menu or Task Manager is open.
            self._logger.debug("No active windows.")
            return None
        # active_windows = desktop.windows(active_only=True)
        # if not active_windows:
        # 	# This can happen when the Start Menu or Task Manager is open.
        # 	self._logger.debug("No active windows.")
        # 	return None
        # active_window = active_windows[0]
        assert active_window.is_active()
        # window_title = active_window.window_text()
        active_window.element_info
        window_title = active_window.element_info.name
        # active_window.element_info.rich_text (but can  be the same as `name`)
        assert isinstance(window_title, str), f"Expected a string for `window_title`, got `{type(window_title)}` instead."

        process_id = active_window.element_info.process_id
        assert isinstance(process_id, int), f"Expected an int for `process_id`, got `{type(process_id)}` instead."
        process = Process(process_id)
        process_name = process.name()
        # full_path = process.exe()

        self._logger.info("Active window title: \"%s\" (%s)",
                          window_title, process_name)
        # active_window.process_id()
        # Some other info:
        # [(p, getattr(active_window, p)()) for p in active_window.writable_props]
        # TODO Get program name.

        # TODO Get more information about the windows like text they're entering in input fields.
        # TODO Figure more ways to get input elements.
        # input_elements = active_window.descendants(control_type='Edit')
        # for i in input_elements:
        # 	self._logger.info("Input element: %s", i)
        result = WindowInfo(
            title=window_title,
            process_name=process_name,
        )

        self._logger.debug("Active window: %s", result)

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
