from abc import ABC, abstractmethod
from src.database_objects.row import Row

class ConstraintViolationException(Exception):
    pass

class IConstraintValidator(ABC):
    @abstractmethod
    def validate(self, row: Row) -> None:
        pass

class NotNullValidator(IConstraintValidator):
    def __init__(self, column_index: int):
        self.column_index = column_index

    def validate(self, row: Row) -> None:
        raise NotImplementedError()

class UniqueValidator(IConstraintValidator):
    def __init__(self, column_index: int):
        self.column_index = column_index

    def validate(self, row: Row) -> None:
        raise NotImplementedError()
