import pytest
from src.database_objects.table import Table, DuplicateColumnException, ColumnNotFoundException, RowSchemaMismatchException
from src.database_objects.column import Column
from src.database_objects.row import Row
from src.database_objects.constraint import NotNullValidator
from unittest.mock import MagicMock

class TestAddColumn:
    def test_AddColumn_WhenColumnIsValid_ShouldAddColumn(self):
        table = Table("users")
        col = Column("id", "integer")
        table.add_column(col)
        assert table.contains_column("id") is True
        assert table.get_column("id") == col

    def test_AddColumn_WhenNameAlreadyExists_ShouldThrow(self):
        table = Table("users")
        col1 = Column("id", "integer")
        col2 = Column("id", "string")
        table.add_column(col1)
        with pytest.raises(DuplicateColumnException):
            table.add_column(col2)


class TestDropColumn:
    def test_DropColumn_WhenColumnExists_ShouldRemoveColumn(self):
        table = Table("test_table")
        col = Column("id", "int")
        table.add_column(col)
        table.drop_column("id")
        assert table.contains_column("id") is False


class TestRowOperations:
    def test_InsertRow_WhenRowIsValid_ShouldInsertRow(self):
        table = Table("users")
        table.add_column(Column("id", "integer"))
        row = Row([1])
        table.insert_row(row)
        assert table.contains_row(row) is True
        assert len(table._rows) == 1

    def test_InsertRow_WhenValueCountDoesNotMatch_ShouldThrow(self):
        table = Table("users")
        table.add_column(Column("id", "integer"))
        table.add_column(Column("name", "string"))
        row = Row([1])
        with pytest.raises(RowSchemaMismatchException):
            table.insert_row(row)

    def test_InsertRow_StrategyPattern_ShouldDelegateToValidator(self):
        table = Table("users")
        table.add_column(Column("id", "integer"))
        
        mock_validator = MagicMock()
        table.add_validator(mock_validator)
        
        row = Row([1])
        table.insert_row(row)
        mock_validator.validate.assert_called_once_with(row)


class TestIndexIntegration:
    def test_AddIndex_ShouldStoreInTable(self):
        table = Table("users")
        mock_index = MagicMock()
        table.add_index(mock_index)
        assert mock_index in table._indexes

    def test_GetPrimaryIndex_ShouldReturnCorrectIndex(self):
        table = Table("users")
        mock_index = MagicMock()
        mock_index.is_primary = True
        table.add_index(mock_index)
        primary = table.get_primary_index()
        assert primary == mock_index
