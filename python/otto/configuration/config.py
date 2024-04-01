from dataclasses import dataclass

from otto.ai.sk.sk_config import SKConfig


@dataclass
class Config:
    log_level: str | int | None
    global_log_level: str | int | None

    # Maybe it's bad to force everything into one config file.
    # It's fine when things are small, but we may split stuff into other files later if it gets too big.
    sk: SKConfig
