from pywinauto import Application

from chat.message import ChatMessage

# Some examples that might be helpful:
# General stuff about pywinauto: https://pywinauto.readthedocs.io/en/latest/getting_started.html
# Specific to Microsoft Teams:
# https://www.reddit.com/r/learnpython/comments/q46o03/pywinauto_controlling_microsoft_teams_getting/
# https://github.com/pywinauto/pywinauto/discussions/1236


class MicrosoftTeams:
	def __init__(self):
		self.app = Application(backend='uia') \
			.connect(title_re=r'.* \| Microsoft Teams$')

	def get_messages(self) -> list[ChatMessage]:
		# Get the latest version of the window.
		window_spec = self.app.window()
		assert window_spec.wrapper_object(), "Not found."
		app_window = window_spec.child_window(auto_id='app', control_type='Group')
		assert app_window.wrapper_object(), "Not found."
		# TODO
		raise NotImplementedError("Not implemented yet.")

	def type_message(self, message: str, send_message=False) -> None:
		# Get the latest version of the window.
		window_spec = self.app.window()
		assert window_spec.wrapper_object(), "Not found."
		app_window = window_spec.child_window(auto_id='app', control_type='Group')
		assert app_window.wrapper_object(), "Not found."
		input_element = app_window.child_window(control_type='Edit')
		# Without focus, sometimes the first characters get dropped.
		input_element.set_focus()
		if send_message:
			message += '{ENTER}'
		input_element.type_keys(message, with_spaces=True, with_newlines=True)
