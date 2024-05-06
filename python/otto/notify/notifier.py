from typing import Optional
from plyer import notification
from plyer.facades import Notification

from otto.msteams.msteams_control import MicrosoftTeams


class Notifier:
    def notify(self,
               message: str,
               display_seconds: Optional[int] = None) \
            -> None:
        if display_seconds is None:
            display_seconds = max(5, int(len(message) * 0.5))

        plyer_notifier: Notification = notification  # type: ignore
        plyer_notifier.notify(
            title="Pilot",
            # app_icon=icon_path,
            message=message,
            app_name="Pilot",
            timeout=display_seconds,
        )


if __name__ == '__main__':
    import time
    import threading

    def type_message():
        time.sleep(1)
        MicrosoftTeams().type_message("Join the \"Gen AI\" security group.", send_message=False)

    # thread = threading.Thread(target=type_message)
    # thread.start()
    n = Notifier()
    n.notify("Tell them: .", display_seconds=4)

    # thread.join()
