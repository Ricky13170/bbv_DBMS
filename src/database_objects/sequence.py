class Sequence:
    def __init__(self, name: str, start: int = 1, increment: int = 1):
        self.name = name
        self.start = start
        self.increment = increment
        self._current_value = start

    def next_value(self) -> int:
        raise NotImplementedError()
