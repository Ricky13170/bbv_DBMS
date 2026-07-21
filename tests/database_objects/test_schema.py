import pytest
from src.database_objects.schema import (
    Schema,
    DuplicateTableNameException,
    TableNotFoundException
)
from src.database_objects.table import Table


class TestAddTable:
    def test_AddTable_WhenTableIsValid_ShouldRegisterTable(self):
        schema = Schema("public")
        table = Table("users")
        
        schema.add_table(table)
        
        assert schema.contains_table("users") is True
        assert schema.get_table("users") == table

    def test_AddTable_WhenNameAlreadyExists_ShouldThrow(self):
        schema = Schema("public")
        table1 = Table("users")
        table2 = Table("users")
        
        schema.add_table(table1)
        
        with pytest.raises(DuplicateTableNameException):
            schema.add_table(table2)


class TestGetTable:
    def test_GetTable_WhenTableNotFound_ShouldThrow(self):
        schema = Schema("public")
        
        with pytest.raises(TableNotFoundException):
            schema.get_table("non_existent_table")


class TestRemoveTable:
    def test_RemoveTable_WhenTableExists_ShouldRemoveTable(self):
        schema = Schema("public")
        table = Table("users")
        
        # Override to bypass NotImplementedError for setup (or use mock)
        # But wait, in purely strict TDD we want the actual method to fail 
        # so this test will fail at add_table before it even reaches remove_table.
        # That's perfectly fine for Red Phase.
        schema.add_table(table)
        schema.remove_table("users")
        
        assert schema.contains_table("users") is False

    def test_RemoveTable_WhenTableNotFound_ShouldThrow(self):
        schema = Schema("public")
        
        with pytest.raises(TableNotFoundException):
            schema.remove_table("non_existent_table")
