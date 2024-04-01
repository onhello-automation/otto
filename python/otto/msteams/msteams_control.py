from pywinauto import Application, WindowSpecification

from otto.chat.message import ChatMessage

# Some examples that might be helpful:
# General stuff about pywinauto: https://pywinauto.readthedocs.io/en/latest/getting_started.html
# Specific to Microsoft Teams:
# https://www.reddit.com/r/learnpython/comments/q46o03/pywinauto_controlling_microsoft_teams_getting/
# https://github.com/pywinauto/pywinauto/discussions/1236


class MicrosoftTeams:
    process_name = 'msteams.exe'

    def __init__(self):
        self.app = Application(backend='uia') \
            .connect(title_re=r'^[^|]* \| [^|]* \| Microsoft Teams$')

    def get_messages(self) -> list[ChatMessage]:
        # Get the latest version of the window.
        window_spec = self.app.window()
        assert window_spec.exists(), "Not found."
        app_window = window_spec.child_window(auto_id='app', control_type='Group')
        assert app_window.exists(), "Not found."
        return self.get_messages_from_window(app_window)

    @classmethod
    def get_messages_from_window(cls, window_spec: WindowSpecification) -> list[ChatMessage]:
        # TODO Get messages.
        # messages = window_spec.descendants(auto_id='app', control_type='Group')
        messages = window_spec.child_window(control_type='Main')
        # print(messages)
        # assert messages.wrapper_object(), "Could not find messages wrapper object."
        assert messages.exists(), "messages does not exist."
        # TODO
        # messages = messages.child_window(auto_id='app', control_type='Main')
        print(messages.window_text())
        print(messages.title)
        print(messages.title())
        # messages.print_control_identifiers()
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
