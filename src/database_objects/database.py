from abc import ABC, abstractmethod
from src.database_objects.catalog_manager import CatalogManager
from src.database_objects.schema import Schema
from src.database_objects.schema_builder import SchemaBuilder

class IDatabase(ABC):
    """Abstract Product"""
    @abstractmethod
    def create_schema(self, schema_name: str) -> None: pass
    
    @abstractmethod
    def drop_schema(self, schema_name: str) -> None: pass
    
    @abstractmethod
    def get_schema(self, schema_name: str) -> Schema: pass

class RelationalDatabase(IDatabase):
    """Concrete Product"""
    def __init__(self, name: str):
        self.name = name
        self._catalog = CatalogManager()

    def create_schema(self, schema_name: str) -> None:
        raise NotImplementedError()

    def drop_schema(self, schema_name: str) -> None:
        raise NotImplementedError()

    def get_schema(self, schema_name: str) -> Schema:
        raise NotImplementedError()
