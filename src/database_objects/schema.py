from .table import Table


class DuplicateTableNameException(Exception):
    pass


class TableNotFoundException(Exception):
    pass


class Schema:
    def __init__(self, name: str):
        self.name = name
        self._tables = {}

    def add_table(self, table: Table) -> None:
        if table.name in self._tables:
            raise DuplicateTableNameException(f"Table '{table.name}' already exists.")
        self._tables[table.name] = table

    def get_table(self, table_name: str) -> Table:
        if table_name not in self._tables:
            raise TableNotFoundException(f"Table '{table_name}' does not exist.")
        return self._tables[table_name]

    def remove_table(self, table_name: str) -> None:
        if table_name not in self._tables:
            raise TableNotFoundException(f"Table '{table_name}' does not exist.")
        del self._tables[table_name]

    def contains_table(self, table_name: str) -> bool:
        return table_name in self._tables
