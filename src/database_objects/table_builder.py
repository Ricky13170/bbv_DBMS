from .table import Table
from .column import Column


class InvalidTableDefinitionException(Exception):
    pass


class TableBuilder:
    def __init__(self, table_name: str):
        self._table = Table(table_name)

    def with_int_column(self, name: str) -> 'TableBuilder':
        self._table.add_column(Column(name, "integer"))
        return self

    def with_string_column(self, name: str, length: int) -> 'TableBuilder':
        self._table.add_column(Column(name, f"string({length})"))
        return self

    def build(self) -> Table:
        if len(self._table._columns) == 0:
            raise InvalidTableDefinitionException("Table must have at least one column.")
        return self._table
