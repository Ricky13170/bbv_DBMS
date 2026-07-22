from src.database_objects.table import Table

class TableBuilder:
    def __init__(self, table_name: str):
        self.table_name = table_name

    def with_column(self, name: str, data_type: str) -> 'TableBuilder':
        raise NotImplementedError()

    def with_int_column(self, name: str) -> 'TableBuilder':
        raise NotImplementedError()

    def with_string_column(self, name: str) -> 'TableBuilder':
        raise NotImplementedError()

    def build(self) -> Table:
        raise NotImplementedError()
