import pytest
from src.database_objects.schema_builder import SchemaBuilder
from src.database_objects.schema import Schema

class TestSchemaBuilder:
    def test_Build_ShouldReturnProperlyConstructedSchemaTree(self):
        builder = SchemaBuilder("analytics")
        builder.with_table("users").with_string_column("id")
        builder.with_table("sales").with_int_column("amount")
        
        schema = builder.build()
        
        assert schema is not None
        assert schema.name == "analytics"
        assert schema.get_table("users") is not None
        assert schema.get_table("sales") is not None

    def test_WithTable_EmptyName_ShouldRaiseValueError(self):
        builder = SchemaBuilder("analytics")
        with pytest.raises(ValueError):
            builder.with_table("")

    def test_Build_EmptySchemaName_ShouldRaiseValueError(self):
        with pytest.raises(ValueError):
            SchemaBuilder("")
