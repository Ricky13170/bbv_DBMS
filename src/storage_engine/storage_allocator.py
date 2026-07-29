from typing import List, Optional
from .page_manager import PageID


class OutOfSpaceException(Exception): pass
class InvalidExtentException(Exception): pass


class StorageAllocator:
    """
    Singleton — exactly one free-space bitmap manager per engine instance.
    Prevents double-allocation of the same physical page.
    """
    _instance: Optional['StorageAllocator'] = None

    def __init__(self, total_pages: int):
        if StorageAllocator._instance is not None:
            raise RuntimeError("Use StorageAllocator.get_instance() instead.")
        self._total_pages: int = total_pages
        self._free_bitmap: List[bool] = [True] * total_pages

    @classmethod
    def get_instance(cls, total_pages: int = 1024) -> 'StorageAllocator':
        if cls._instance is None:
            cls._instance = cls(total_pages)
        return cls._instance

    def allocate_extent(self, n_pages: int) -> List[PageID]:
        raise NotImplementedError()

    def release_extent(self, page_ids: List[PageID]) -> None:
        raise NotImplementedError()

    def get_free_space(self) -> int:
        """Returns the number of free pages remaining."""
        raise NotImplementedError()
