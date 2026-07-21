import pytest
from src.database_objects.table_builder import TableBuilder, InvalidTableDefinitionException
from src.database_objects.table import Table


class TestTableBuilder:
    def test_Build_WhenAddingColumns_ShouldReturnConfiguredTable(self):
        builder = TableBuilder("users")
        
        # Fluent interface chaining
        table = (builder
                 .with_int_column("id")
                 .with_string_column("name", 50)
                 .build())
        
        assert table.name == "users"
        assert table.contains_column("id") is True
        assert table.contains_column("name") is True
        
        assert table.get_column("id").type == "integer"
        assert table.get_column("name").type == "string(50)"

    def test_Build_WhenNoColumnsAdded_ShouldThrow(self):
        builder = TableBuilder("empty_table")
        
        with pytest.raises(InvalidTableDefinitionException):
            builder.build()
