from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, Optional, Callable, TYPE_CHECKING

if TYPE_CHECKING:
    from src.database_objects.row import Row
    from src.database_objects.table import Table
    from src.database_objects.schema import Schema


class ConstraintViolationException(Exception):
    pass



class ConstraintContext:
    def __init__(
        self,
        candidate_row: "Row",
        table: "Table",
        schema: "Schema",
        existing_row: Optional["Row"] = None,
    ):
        self.candidate_row = candidate_row
        self.existing_row = existing_row
        self.table = table
        self.schema = schema


# Abstract Constraint
class Constraint(ABC):
    def __init__(self, name: str):
        self.name = name
        self.is_enabled: bool = True

    def enable(self) -> None:
        self.is_enabled = True

    def disable(self) -> None:
        self.is_enabled = False

    def validate(self, context: ConstraintContext) -> bool:
        """Public entry point — skips disabled constraints."""
        if not self.is_enabled:
            return True
        return self._check(context)

    @abstractmethod
    def _check(self, context: ConstraintContext) -> bool:
        """Concrete strategy logic implemented by each subclass."""


# Concrete Constraints
class CheckConstraint(Constraint):
    """Validates an arbitrary predicate against the candidate row."""

    def __init__(self, name: str, predicate: Callable[["Row"], bool]):
        super().__init__(name)
        self.predicate = predicate

    def _check(self, context: ConstraintContext) -> bool:
        raise NotImplementedError()


class UniqueConstraint(Constraint):
    """Ensures no two rows share identical values across the given columns."""

    def __init__(self, name: str, column_names: List[str]):
        super().__init__(name)
        self.column_names = column_names

    def _check(self, context: ConstraintContext) -> bool:
        raise NotImplementedError()


class PrimaryKeyConstraint(Constraint):
    """Combination of Unique + NotNull across the primary-key columns."""

    def __init__(self, name: str, column_names: List[str]):
        super().__init__(name)
        self.column_names = column_names

    def _check(self, context: ConstraintContext) -> bool:
        raise NotImplementedError()



class IReferentialAction(ABC):
    """Defines what happens to child rows when the parent is deleted/updated."""

    @abstractmethod
    def execute(self, parent_row: "Row", child_table: "Table") -> None:
        pass


class CascadeAction(IReferentialAction):
    """Delete / update child rows automatically."""

    def execute(self, parent_row: "Row", child_table: "Table") -> None:
        raise NotImplementedError()


class RestrictAction(IReferentialAction):
    """Raise an error if matching child rows still exist."""

    def execute(self, parent_row: "Row", child_table: "Table") -> None:
        raise NotImplementedError()


class SetNullAction(IReferentialAction):
    """Set the child FK column to NULL."""

    def execute(self, parent_row: "Row", child_table: "Table") -> None:
        raise NotImplementedError()


# ForeignKeyConstraint
class ForeignKeyConstraint(Constraint):
    """
    Enforces referential integrity.
    on_delete / on_update accept any IReferentialAction strategy.
    """

    def __init__(
        self,
        name: str,
        child_column_name: str,
        referenced_table_name: str,
        referenced_column_name: str,
        on_delete: IReferentialAction,
        on_update: IReferentialAction,
        is_nullable: bool = False,
    ):
        super().__init__(name)
        self.child_column_name = child_column_name
        self.referenced_table_name = referenced_table_name
        self.referenced_column_name = referenced_column_name
        self.on_delete = on_delete
        self.on_update = on_update
        self.is_nullable = is_nullable

    def _check(self, context: ConstraintContext) -> bool:
        raise NotImplementedError()

    def on_parent_row_deleted(self, parent_row: "Row", child_table: "Table") -> None:
        raise NotImplementedError()
