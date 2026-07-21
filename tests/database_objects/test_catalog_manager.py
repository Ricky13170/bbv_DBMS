import pytest
from src.database_objects.catalog_manager import CatalogManager
from src.database_objects.schema import Schema

class TestCatalogManager:
    def test_Singleton_WhenCalledMultipleTimes_ShouldReturnSameInstance(self):
        instance1 = CatalogManager()
        instance2 = CatalogManager()
        
        # Verify both point to identical memory address
        assert instance1 is instance2

    def test_AddAndGetSchema_ShouldWorkAcrossInstances(self):
        manager1 = CatalogManager()
        schema = Schema("public")
        manager1.add_schema(schema)
        
        # Fetching through a "new" call should still return the same shared data
        manager2 = CatalogManager()
        fetched_schema = manager2.get_schema("public")
        
        assert fetched_schema is schema
