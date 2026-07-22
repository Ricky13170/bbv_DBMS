from typing import Optional, List, Any


class IndexEntry:
    """Stores a single key with its associated record pointers."""
    def __init__(self, key: Any, record_pointers: List[Any]):
        self.key = key
        self.record_pointers: List[Any] = list(record_pointers)


class Index:
    """Base index structure. Subclasses (BTree, Hash) override search logic."""

    def __init__(self, name: str, columns: List[str],
                 is_unique: bool = False, allows_null: bool = True):
        self.name = name
        self.columns = columns
        self.is_unique = is_unique
        self.allows_null = allows_null
        self._entries: dict[Any, List[Any]] = {}

    # ── Write operations ────────────────────────────────────────────────────

    def insert(self, key: Any, record_pointer: Any) -> None:
        """Insert a key → record pointer mapping into the index."""
        raise NotImplementedError()

    def update(self, key: Any, new_record_pointer: Any) -> None:
        """Replace the record pointer for an existing key."""
        raise NotImplementedError()

    def delete(self, key: Any) -> bool:
        """Remove a key. Returns True if removed, False if not found."""
        raise NotImplementedError()


    def search(self, key: Any) -> Optional[Any]:
        """Point lookup. Returns record pointer or None."""
        raise NotImplementedError()

    def range_search(self, start_key: Any, end_key: Any) -> List[Any]:
        """Range scan. Returns ordered list of record pointers."""
        raise NotImplementedError()


class BTreeIndex(Index):
    """B-Tree index — supports both point and range lookups."""
    pass


class HashIndex(Index):
    """Hash index — O(1) point lookup, no range support."""
    pass


class IndexFactory:
    """
    Factory Method pattern.
    Creates the correct Index subtype based on the `index_type` flag.
    Raises ValueError for unrecognised index types.
    """

    SUPPORTED_TYPES = {"BTREE", "HASH"}

    @staticmethod
    def create_index(index_type: str, name: str, columns: List[str],
                     is_unique: bool = False) -> Index:
        raise NotImplementedError()
