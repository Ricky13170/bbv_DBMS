import pytest
from src.database_objects.column import Column


class TestColumnCreation:

    def test_Create_WhenDefinitionIsValid_ShouldCreateColumn(self):
        col = Column("user_id", "int")
        assert col.name == "user_id"
        assert col.data_type == "int"
        assert col.is_nullable is True  # default

    def test_Create_WhenNullableIsFalse_ShouldStoreFlag(self):
        col = Column("email", "str", is_nullable=False)
        assert col.is_nullable is False

    def test_Create_WhenNameIsEmpty_ShouldThrow(self):
        with pytest.raises(ValueError):
            Column("", "int")

    def test_Create_WhenDataTypeIsInvalid_ShouldThrow(self):
        with pytest.raises(ValueError):
            Column("col", "varchar")  # not in SUPPORTED_TYPES


class TestColumnImmutability:

    def test_Name_ShouldBeReadOnly(self):
        col = Column("id", "int")
        with pytest.raises(AttributeError):
            col.name = "changed"

    def test_DataType_ShouldBeReadOnly(self):
        col = Column("id", "int")
        with pytest.raises(AttributeError):
            col.data_type = "str"

    def test_IsNullable_ShouldBeReadOnly(self):
        col = Column("id", "int", is_nullable=False)
        with pytest.raises(AttributeError):
            col.is_nullable = True


class TestColumnEquality:

    def test_Equality_WhenSameNameTypeNullable_ShouldBeEqual(self):
        col1 = Column("id", "int", is_nullable=False)
        col2 = Column("id", "int", is_nullable=False)
        assert col1 == col2

    def test_Equality_WhenDifferentNullable_ShouldNotBeEqual(self):
        col1 = Column("id", "int", is_nullable=True)
        col2 = Column("id", "int", is_nullable=False)
        assert col1 != col2

    def test_Equality_WhenDifferentName_ShouldNotBeEqual(self):
        col1 = Column("id", "int")
        col2 = Column("user_id", "int")
        assert col1 != col2

    def test_Hash_WhenEqualColumns_ShouldHaveSameHash(self):
        col1 = Column("id", "int", is_nullable=False)
        col2 = Column("id", "int", is_nullable=False)
        assert hash(col1) == hash(col2)


class TestColumnValidateValue:

    def test_ValidateValue_WhenTypeMatches_ShouldReturnTrue(self):
        col = Column("age", "int")
        assert col.validate_value(42) is True

    def test_ValidateValue_WhenTypeDoesNotMatch_ShouldReturnFalse(self):
        col = Column("age", "int")
        assert col.validate_value("not_an_int") is False

    def test_ValidateValue_WhenValueIsNullAndNullable_ShouldReturnTrue(self):
        col = Column("middle_name", "str", is_nullable=True)
        assert col.validate_value(None) is True

    def test_ValidateValue_WhenValueIsNullAndNotNullable_ShouldReturnFalse(self):
        col = Column("email", "str", is_nullable=False)
        assert col.validate_value(None) is False
