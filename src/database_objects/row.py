from typing import List, Any, Tuple

class Row:
    def __init__(self, values: List[Any]):
        self._values: Tuple = tuple(values)

    @property
    def values(self) -> Tuple:
        return self._values

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Row):
            return NotImplemented
        return self._values == other.values

    def __hash__(self) -> int:
        return hash(self._values)
