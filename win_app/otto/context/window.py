from dataclasses import dataclass


@dataclass
class WindowInfo:
    process_name: str
    """
	The name of the program.
	E.g., "Code.exe" for VS Code or "msedge.exe" for the Edge browser.
	"""

    title: str
    """
	The visible title on the window.
	"""
