from src.database_objects.schema import Schema
from src.database_objects.table_builder import TableBuilder

class SchemaBuilder:
    def __init__(self, name: str):
        self.name = name
        self._table_builders = []

    def with_table(self, table_name: str) -> TableBuilder:
        raise NotImplementedError()

    def build(self) -> Schema:
        raise NotImplementedError()
