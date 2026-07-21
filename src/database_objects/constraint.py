from abc import ABC, abstractmethod
from typing import Any
from .row import Row


class ConstraintViolationException(Exception):
    pass


class IConstraintValidator(ABC):
    @abstractmethod
    def validate(self, row: Row) -> bool:
        pass


class NotNullValidator(IConstraintValidator):
    def __init__(self, column_index: int):
        self.column_index = column_index

    def validate(self, row: Row) -> bool:
        if row.values[self.column_index] is None:
            raise ConstraintViolationException("Null value is not allowed.")
        return True


class UniqueValidator(IConstraintValidator):
    def __init__(self, column_index: int):
        self.column_index = column_index
        # Internal state to track keys seen so far in this session/table
        self._seen_values = set()

    def validate(self, row: Row) -> bool:
        val = row.values[self.column_index]
        if val in self._seen_values:
            raise ConstraintViolationException(f"Duplicate value '{val}' violates unique constraint.")
        self._seen_values.add(val)
        return True
