from enum import Enum

class VmState(Enum):
    FAILURE = -10
    NEW = 10
    READY = 20
    LOCKED = 30
    MARKED_FOR_DEATH = 40
