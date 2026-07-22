from typing import List, Optional
from src.database_objects.column import Column
from src.database_objects.row import Row
from src.database_objects.index_factory import Index
from src.database_objects.constraint import Constraint
from src.database_objects.database_object import DatabaseObject
class DuplicateColumnException(Exception): pass
class ColumnNotFoundException(Exception): pass
class RowSchemaMismatchException(Exception): pass
class ConstraintNotFoundException(Exception): pass
class ColumnReferencedException(Exception): pass

class Table(DatabaseObject):
    def __init__(self, name: str):
        super().__init__(name)
        self._columns: List[Column] = []
        self._rows: List[Row] = []
        self._constraints: List[Constraint] = []
        self._indexes: List[Index] = []

    def add_column(self, column: Column) -> None:
        raise NotImplementedError()

    def create(self) -> None:
        raise NotImplementedError()

    def drop(self) -> None:
        raise NotImplementedError()

    def drop_column(self, column_name: str) -> None:
        raise NotImplementedError()

    def add_constraint(self, constraint: Constraint) -> None:
        raise NotImplementedError()

    def drop_constraint(self, name: str) -> None:
        raise NotImplementedError()

    def alter_column(self, column_name: str, new_column: Column) -> None:
        raise NotImplementedError()

    def get_column(self, column_name: str) -> Column:
        raise NotImplementedError()

    def contains_column(self, column_name: str) -> bool:
        raise NotImplementedError()

    def insert_row(self, row: Row) -> None:
        raise NotImplementedError()

    def update_row(self, old_row: Row, new_row: Row) -> None:
        raise NotImplementedError()

    def delete_row(self, row: Row) -> bool:
        raise NotImplementedError()

    def contains_row(self, row: Row) -> bool:
        raise NotImplementedError()

    def add_index(self, index: Index) -> None:
        raise NotImplementedError()

    def get_primary_index(self) -> Optional[Index]:
        raise NotImplementedError()

    def accept(self, visitor) -> None:
        raise NotImplementedError()
