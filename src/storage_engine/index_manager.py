from typing import Dict
from src.database_objects.index_factory import Index, IndexFactory


class IndexNotFoundException(Exception): pass
class IndexAlreadyExistsException(Exception): pass


class IndexManager:
    """
    Factory Method — orchestrates the lifecycle (create / drop / rebuild)
    of all physical indexes by delegating construction to IndexFactory.
    """

    def __init__(self):
        self._indexes: Dict[str, Index] = {}
        self._factory: IndexFactory = IndexFactory()

    def create_index(self, idx_type: str, name: str) -> Index:
        raise NotImplementedError()

    def drop_index(self, name: str) -> None:
        raise NotImplementedError()

    def rebuild_index(self, name: str) -> None:
        raise NotImplementedError()

    def get_index(self, name: str) -> Index:
        raise NotImplementedError()
