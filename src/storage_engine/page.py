from .page_manager import PageID


class Page:
    """
    Value Object — represents a 4 KB in-memory unit of data read from disk.
    Held inside a BufferPool frame. Tracks dirty state and pin count.
    """
    PAGE_SIZE = 4096

    def __init__(self, page_id: PageID, data: bytes):
        self.page_id: PageID = page_id
        self._data: bytes = data
        self.is_dirty: bool = False
        self.pin_count: int = 0

    def get_data(self) -> bytes:
        raise NotImplementedError()

    def set_data(self, data: bytes) -> None:
        raise NotImplementedError()

    def mark_dirty(self) -> None:
        raise NotImplementedError()

    def pin(self) -> None:
        raise NotImplementedError()

    def unpin(self) -> None:
        raise NotImplementedError()
