import pytest
from src.database_objects.table import (
    Table,
    DuplicateColumnException,
    ColumnMismatchException
)
from src.database_objects.column import Column
from src.database_objects.row import Row


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


class TestInsertRow:
    def test_InsertRow_WhenRowMatchesColumnCount_ShouldAddRow(self, mocker):
        table = Table("users")
        col1 = Column("id", "integer")
        col2 = Column("name", "string")
        
        # Override add_column so we can feed in metadata for this specific test
        # without it failing from NotImplementedError (which is inside add_column)
        def mock_add_column(col):
            table._columns[col.name] = col
        
        mocker.patch.object(table, 'add_column', side_effect=mock_add_column)
        table.add_column(col1)
        table.add_column(col2)
        
        row = Row([1, "Alice"])
        table.insert_row(row)
        
        assert len(table._rows) == 1

    def test_InsertRow_WhenValueCountDoesNotMatch_ShouldThrow(self, mocker):
        table = Table("users")
        col = Column("id", "integer")
        
        def mock_add_column(col):
            table._columns[col.name] = col
        mocker.patch.object(table, 'add_column', side_effect=mock_add_column)
        table.add_column(col)
        
        # Row has 2 values, but table only expects 1 from the registered columns
        row = Row([1, "Alice"])
        
        with pytest.raises(ColumnMismatchException):
            table.insert_row(row)


class TestInsertRowWithConstraints:
    def test_InsertRow_WhenValidatorFails_ShouldThrow(self, mocker):
        from src.database_objects.constraint import NotNullValidator, ConstraintViolationException
        table = Table("users")
        col = Column("id", "integer")
        
        def mock_add_column(col):
            table._columns[col.name] = col
        mocker.patch.object(table, 'add_column', side_effect=mock_add_column)
        table.add_column(col)
        
        # Inject the constraint strategy
        validator = NotNullValidator(0)
        table.add_validator(validator)
        
        row = Row([None]) # Null violates the constraint
        
        # Because Table.insert_row currently lacks the logic to loop through validators,
        # it will incorrectly accept the Null row and fail to raise the exception,
        # fulfilling the Red Phase of Pytest!
        with pytest.raises(ConstraintViolationException):
            table.insert_row(row)
