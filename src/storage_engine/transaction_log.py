from abc import ABC, abstractmethod

class ILogRecord(ABC):
    """Command — encapsulates a database mutation for Undo/Redo recovery."""

    @abstractmethod
    def execute(self) -> None:
        """Redo the operation."""
        raise NotImplementedError()

    @abstractmethod
    def undo(self) -> None:
        """Rollback the operation."""
        raise NotImplementedError()

class InsertLog(ILogRecord):
    def execute(self) -> None:
        raise NotImplementedError()

    def undo(self) -> None:
        raise NotImplementedError()

class UpdateLog(ILogRecord):
    def execute(self) -> None:
        raise NotImplementedError()

    def undo(self) -> None:
        raise NotImplementedError()

class DeleteLog(ILogRecord):
    def execute(self) -> None:
        raise NotImplementedError()

    def undo(self) -> None:
        raise NotImplementedError()
