from src.database_objects.catalog_manager import CatalogManager
from src.database_objects.schema import Schema
from src.database_objects.schema_builder import SchemaBuilder

class Database:
    def __init__(self, name: str):
        self.name = name
        self._catalog = CatalogManager()

    def create_schema(self, schema_name: str) -> None:
        raise NotImplementedError()

    def drop_schema(self, schema_name: str) -> None:
        raise NotImplementedError()

    def get_schema(self, schema_name: str) -> Schema:
        raise NotImplementedError()
