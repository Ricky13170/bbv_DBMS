from src.database_objects.database_object import DatabaseObject

class Sequence(DatabaseObject):
    def __init__(self, name: str, start: int = 1, increment: int = 1):
        super().__init__(name)
        self.start = start
        self.increment = increment
        self._current_value = start

    def create(self) -> None:
        raise NotImplementedError()

    def drop(self) -> None:
        raise NotImplementedError()

    def next_value(self) -> int:
        raise NotImplementedError()
