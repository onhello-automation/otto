from dataclasses import dataclass


@dataclass
class Config:
	log_level: str | int | None
