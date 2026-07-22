import pytest
from src.database_objects.catalog_manager import CatalogManager
from src.database_objects.schema import Schema

class TestCatalogManager:
    def setup_method(self):
        # Reset the singleton before tests
        CatalogManager._instance = None

    def test_Singleton_ShouldReturnSameAddress(self):
        c1 = CatalogManager()
        c2 = CatalogManager()
        assert c1 is c2

    def test_AddSchema_ShouldPersistGlobally(self):
        c1 = CatalogManager()
        c1.add_schema(Schema("global_schema"))
        
        c2 = CatalogManager()
        retrieved = c2.get_schema("global_schema")
        
        assert retrieved is not None
        assert retrieved.name == "global_schema"
