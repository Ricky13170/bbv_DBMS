from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from .page import Page
from .page_manager import PageID, PageManager


class IEvictionPolicy(ABC):
    """Strategy — defines the algorithm to select a victim frame for eviction."""

    @abstractmethod
    def record_access(self, page_id: PageID) -> None:
        raise NotImplementedError()

    @abstractmethod
    def select_victim(self) -> Optional[PageID]:
        raise NotImplementedError()

    @abstractmethod
    def remove(self, page_id: PageID) -> None:
        raise NotImplementedError()


class LRUPolicy(IEvictionPolicy):
    """Least Recently Used eviction strategy."""

    def __init__(self):
        self._access_order: List[PageID] = []

    def record_access(self, page_id: PageID) -> None:
        raise NotImplementedError()

    def select_victim(self) -> Optional[PageID]:
        raise NotImplementedError()

    def remove(self, page_id: PageID) -> None:
        raise NotImplementedError()


class ClockPolicy(IEvictionPolicy):
    """CLOCK (second-chance) eviction strategy."""

    def __init__(self):
        self._frames: List[PageID] = []
        self._clock_hand: int = 0
        self._reference_bits: Dict[PageID, bool] = {}

    def record_access(self, page_id: PageID) -> None:
        raise NotImplementedError()

    def select_victim(self) -> Optional[PageID]:
        raise NotImplementedError()

    def remove(self, page_id: PageID) -> None:
        raise NotImplementedError()


class BufferPoolFullException(Exception): pass
class PageNotPinnedException(Exception): pass


class BufferPool:
    """
    Proxy — intercepts all page I/O, serving pages from RAM when cached.
    Strategy — delegates eviction decisions to an injected IEvictionPolicy.
    """

    def __init__(self, page_manager: PageManager, capacity: int,
                 eviction_policy: IEvictionPolicy):
        self._page_manager: PageManager = page_manager
        self._capacity: int = capacity
        self._eviction_policy: IEvictionPolicy = eviction_policy
        self._frames: Dict[str, Page] = {} 

    def fetch_page(self, page_id: PageID) -> Page:
        raise NotImplementedError()

    def flush_page(self, page_id: PageID) -> None:
        raise NotImplementedError()

    def flush_all_pages(self) -> None:
        raise NotImplementedError()

    def pin_page(self, page_id: PageID) -> None:
        raise NotImplementedError()

    def unpin_page(self, page_id: PageID) -> None:
        raise NotImplementedError()

    def evict_page(self) -> None:
        raise NotImplementedError()
