from typing import Any, Tuple


class PartitionRangeOverlapException(Exception):
    pass

class PartitionNotFoundException(Exception):
    pass


class PartitionStrategy:
    """
    Manages partition routing and range definitions for a table.
    """
    def __init__(self, partition_key_column: str):
        self.partition_key_column = partition_key_column
        self._ranges: dict[str, Tuple[Any, Any]] = {}

    def add_range(self, partition_name: str, start_key: Any, end_key: Any) -> None:
        """Adds a new range partition."""
        raise NotImplementedError()

    def remove_range(self, partition_name: str) -> None:
        """Removes an existing range partition."""
        raise NotImplementedError()

    def route_row(self, row_key_value: Any) -> str:
        """Returns the partition_name that this key belongs to."""
        raise NotImplementedError()
