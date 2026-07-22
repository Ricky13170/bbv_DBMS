import pytest
from src.database_objects.column import Column

class TestColumn:
    def test_Column_Creation_ShouldStoreNameAndType(self):
        col = Column("user_id", "integer")
        assert col.name == "user_id"
        assert col.type == "integer"

    def test_Column_EqualityByValue_ShouldBeTrueIfSameNameAndType(self):
        col1 = Column("email", "varchar")
        col2 = Column("email", "varchar")
        # Value Object: two columns with same data must be logically equal
        assert col1 == col2

    def test_Column_EqualityByValue_ShouldBeFalseIfDifferentType(self):
        col1 = Column("email", "varchar")
        col2 = Column("email", "integer")
        assert col1 != col2

    def test_Column_Repr_ShouldBeReadable(self):
        col = Column("age", "integer")
        assert "age" in repr(col)
        assert "integer" in repr(col)
