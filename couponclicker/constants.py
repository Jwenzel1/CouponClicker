from enum import Enum, auto


CONFIG_FILE = "config.ini"

class ClipStatuses(Enum):
    SKIPPED = auto()
    ADDED = auto()
    FAILED = auto()
