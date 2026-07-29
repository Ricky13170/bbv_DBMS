from abc import ABC, abstractmethod
from typing import Any, Dict, Iterator, List, Optional
from .buffer_pool import BufferPool
from .page_manager import PageID


class RecordID:
    """Identifies a physical record by its page and slot number."""
    def __init__(self, page_id: PageID, slot: int):
        self.page_id: PageID = page_id
        self.slot: int = slot


class RecordNotFoundException(Exception): pass
class RecordSchemaMismatchException(Exception): pass


class RecordManager(ABC):
    """
    Template Method — defines the invariant skeleton for all record operations.
    Concrete subclasses override _serialize() and _find_free_slot() to provide
    format-specific behaviour (slotted-page, fixed-length, etc.).
    """

    def __init__(self, buffer_pool: BufferPool):
        self._buffer_pool: BufferPool = buffer_pool

    @abstractmethod
    def _find_free_slot(self, table_id: str) -> RecordID:
        raise NotImplementedError()

    @abstractmethod
    def _serialize(self, row: Dict[str, Any]) -> bytes:
        raise NotImplementedError()

    @abstractmethod
    def _deserialize(self, data: bytes) -> Dict[str, Any]:
        raise NotImplementedError()

    def insert_record(self, table_id: str, row: Dict[str, Any]) -> RecordID:
        raise NotImplementedError()

    def read_record(self, record_id: RecordID) -> Dict[str, Any]:
        raise NotImplementedError()

    def update_record(self, record_id: RecordID, new_row: Dict[str, Any]) -> None:
        raise NotImplementedError()

    def delete_record(self, record_id: RecordID) -> None:
        raise NotImplementedError()

    def scan_records(self, table_id: str) -> Iterator[Dict[str, Any]]:
        raise NotImplementedError()
