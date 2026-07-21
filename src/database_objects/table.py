from typing import List, Dict
from .column import Column
from .row import Row
from .constraint import IConstraintValidator, ConstraintViolationException


class DuplicateColumnException(Exception):
    pass


class ColumnMismatchException(Exception):
    pass


class InvalidDataTypeException(Exception):
    pass


class Table:
    def __init__(self, name: str):
        self.name = name
        self._columns: Dict[str, Column] = {}
        self._rows: List[Row] = []
        self._validators: List[IConstraintValidator] = []

    def add_validator(self, validator: IConstraintValidator) -> None:
        self._validators.append(validator)

    def add_column(self, column: Column) -> None:
        if column.name in self._columns:
            raise DuplicateColumnException(f"Column '{column.name}' already exists.")
        self._columns[column.name] = column

    def get_column(self, column_name: str) -> Column:
        if column_name not in self._columns:
            raise KeyError(f"Column '{column_name}' not found.")
        return self._columns[column_name]

    def contains_column(self, column_name: str) -> bool:
        return column_name in self._columns

    def insert_row(self, row: Row) -> None:
        if len(row.values) != len(self._columns):
            raise ColumnMismatchException(
                f"Row length {len(row.values)} does not match table columns {len(self._columns)}."
            )

        for validator in self._validators:
            validator.validate(row)

        self._rows.append(row)

