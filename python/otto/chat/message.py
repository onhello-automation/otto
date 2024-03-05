from dataclasses import dataclass

@dataclass
class ChatMessage:
	"""
	A message in a chat.
	"""
	author: str
	text: str
