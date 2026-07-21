from .schema import Schema
from .table_builder import TableBuilder

class SchemaBuilder:
    def __init__(self, name: str):
        self.name = name
        self._table_builders = []
        
    def with_table(self, table_name: str) -> TableBuilder:
        tb = TableBuilder(table_name)
        self._table_builders.append(tb)
        return tb # Return the child builder for nested chaining
        
    def build(self) -> Schema:
        schema = Schema(self.name)
        # Cascade the build phase downwards to tables
        for tb in self._table_builders:
            schema.add_table(tb.build())
        return schema
