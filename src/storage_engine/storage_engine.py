from enum import Enum
from typing import Optional

from .file_manager import FileManager
from .page_manager import PageManager
from .buffer_pool import BufferPool, IEvictionPolicy, LRUPolicy
from .storage_allocator import StorageAllocator


class EngineStatus(Enum):
    STOPPED = "stopped"
    RUNNING = "running"
    ERROR = "error"


class StorageEngineException(Exception): pass


class StorageEngine:
    def __init__(self):
        self._status: EngineStatus = EngineStatus.STOPPED
        
        # Subsystems shielded by the Facade
        self.file_manager: Optional[FileManager] = None
        self.page_manager: Optional[PageManager] = None
        self.buffer_pool: Optional[BufferPool] = None
        self.storage_allocator: Optional[StorageAllocator] = None

    def initialize(self, max_open_files: int = 100, buffer_capacity: int = 256, total_pages: int = 1024) -> None:
        raise NotImplementedError()

    def shutdown(self) -> None:
        raise NotImplementedError()

    def get_engine_status(self) -> EngineStatus:
        raise NotImplementedError()

