from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

class IRecordIterator(ABC):
    """Iterator — abstracts the traversal of massive datasets without loading them all into RAM."""

    @abstractmethod
    def has_next(self) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def get_next(self) -> Optional[Dict[str, Any]]:
        raise NotImplementedError()

    @abstractmethod
    def reset(self) -> None:
        raise NotImplementedError()

class TableIterator(IRecordIterator):
    def has_next(self) -> bool:
        raise NotImplementedError()

    def get_next(self) -> Optional[Dict[str, Any]]:
        raise NotImplementedError()

    def reset(self) -> None:
        raise NotImplementedError()

class BTreeIterator(IRecordIterator):
    def has_next(self) -> bool:
        raise NotImplementedError()

    def get_next(self) -> Optional[Dict[str, Any]]:
        raise NotImplementedError()

    def reset(self) -> None:
        raise NotImplementedError()
