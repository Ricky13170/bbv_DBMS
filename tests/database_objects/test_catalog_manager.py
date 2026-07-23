import pytest
from src.database_objects.catalog_manager import CatalogManager
from src.database_objects.schema import Schema

class TestCatalogManager:
    def setup_method(self):
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

    def test_AddSchema_WithDuplicateName_ShouldRaiseException(self):
        cm = CatalogManager()
        cm.add_schema(Schema("dup_schema"))
        with pytest.raises(Exception):
            cm.add_schema(Schema("dup_schema"))

    def test_GetSchema_WhenNotExists_ShouldRaiseException(self):
        cm = CatalogManager()
        with pytest.raises(Exception):
            cm.get_schema("ghost_schema")
