from dataclasses import dataclass
from typing import Optional


@dataclass
class ChatMessage:
	"""
	A message in a chat.
	"""
	author_name: str
	author_id: Optional[str]
	text: str
	"""
	The contents of the message.
	"""
