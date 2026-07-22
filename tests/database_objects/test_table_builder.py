import pytest
from src.database_objects.table_builder import TableBuilder
from src.database_objects.table import Table

class TestTableBuilder:
    def test_Build_WhenNoColumnsAdded_ShouldReturnEmptyTable(self):
        builder = TableBuilder("users")
        table = builder.build()
        assert isinstance(table, Table)
        assert table.name == "users"
        assert len(table._columns) == 0

    def test_Build_WhenAddingColumns_ShouldReturnConfiguredTable(self):
        builder = TableBuilder("users")
        table = builder.with_column("id", "int").with_string_column("name").build()
        assert len(table._columns) == 2
        assert table.contains_column("id")
        assert table.contains_column("name")
