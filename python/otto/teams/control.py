from pywinauto import Application
from pywinauto import findwindows

# Some examples that might be helpful:
# General stuff about pywinauto: https://pywinauto.readthedocs.io/en/latest/getting_started.html
# Specific to Microsoft Teams: 
# https://www.reddit.com/r/learnpython/comments/q46o03/pywinauto_controlling_microsoft_teams_getting/
# https://github.com/pywinauto/pywinauto/discussions/1236

class MicrosoftTeams:
	def __init__(self):
		self.app = Application(backend='uia').connect(title_re='.* \| Microsoft Teams$')

	def type_message(self, message: str, send_message = False):
		# Get the latest version of the window.
		window_spec = self.app.window()
		assert window_spec.wrapper_object(), "Not found."
		input_element = window_spec.child_window(control_type="Edit")
		assert input_element.wrapper_object(), "Not found."
		# Without focus, sometimes the first characters get dropped.
		input_element.set_focus()
		if send_message:
			message += '{ENTER}'
		input_element.type_keys(message, with_spaces=True, with_newlines=True)
