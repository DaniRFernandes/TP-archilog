import os

from dataclasses import dataclass


@dataclass
class Config:
    DATABASE_URL: str
    DEBUG: bool

config = Config(
    DATABASE_URL=os.getenv("ARCHILOG_DATABASE_URL", ""),
    DEBUG=os.getenv("ARCHILOG_DEBUG", "False") == "True"
)
