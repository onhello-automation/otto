from dataclasses import dataclass
from typing import Collection


@dataclass
class SKConfig:
    ai_model: str
    embedding_model: str
    knowledge: Collection[str]
    prompt: str
