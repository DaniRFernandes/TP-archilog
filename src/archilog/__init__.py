import logging
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

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("archilog.log"),
        logging.StreamHandler()
    ]
)
