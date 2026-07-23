import pytest
from src.database_objects.database import Database
from src.database_objects.schema import Schema

class TestDatabaseFacade:
    def test_CreateSchema_ShouldGenerateNewSchema(self):
        db = Database("MainDB")
        db.create_schema("public")
        schema = db.get_schema("public")
        
        assert schema is not None
        assert schema.name == "public"
        assert isinstance(schema, Schema)

    def test_DropSchema_ShouldRemoveFromDatabase(self):
        db = Database("MainDB")
        db.create_schema("public")
        db.drop_schema("public")
        
        with pytest.raises(Exception):
            db.get_schema("public")

    def test_CreateSchema_WithDuplicateName_ShouldRaiseException(self):
        db = Database("MainDB")
        db.create_schema("public")
        with pytest.raises(Exception):
            db.create_schema("public")

    def test_GetSchema_WhenNotExists_ShouldRaiseException(self):
        db = Database("MainDB")
        with pytest.raises(Exception):
            db.get_schema("ghost_schema")
