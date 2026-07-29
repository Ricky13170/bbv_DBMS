from enum import Enum


class EngineStatus(Enum):
    STOPPED = "stopped"
    RUNNING = "running"
    ERROR = "error"


class StorageEngineException(Exception): pass


class StorageEngine:
    """
    Facade — provides a single, unified entry point to all Storage Engine subsystems.
    Clients should interact with storage only through this class.
    """

    def __init__(self):
        self._status: EngineStatus = EngineStatus.STOPPED

    def initialize(self) -> None:
        raise NotImplementedError()

    def shutdown(self) -> None:
        raise NotImplementedError()

    def get_engine_status(self) -> EngineStatus:
        raise NotImplementedError()
