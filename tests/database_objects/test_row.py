import pytest
from src.database_objects.row import Row
from src.database_objects.column import Column

class TestRow:
    def test_Row_Creation_ShouldStoreValues(self):
        row = Row([1, "Alice", "alice@email.com"])
        assert row.values[0] == 1
        assert row.values[1] == "Alice"

    def test_Row_EqualityByValue_ShouldBeTrueIfSameValues(self):
        row1 = Row([1, "Alice"])
        row2 = Row([1, "Alice"])
        assert row1 == row2

    def test_Row_EqualityByValue_ShouldBeFalseIfDifferentValues(self):
        row1 = Row([1, "Alice"])
        row2 = Row([2, "Bob"])
        assert row1 != row2

    def test_Row_Immutable_ShouldNotAllowDirectMutation(self):
        row = Row([1, "Alice"])
        with pytest.raises((TypeError, AttributeError)):
            row.values[0] = 99
