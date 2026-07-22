import pytest
from src.database_objects.constraint import (
    NotNullValidator, 
    UniqueValidator,
    ConstraintViolationException
)
from src.database_objects.row import Row


class TestNotNullValidator:
    def test_Validate_WhenValueIsNotNull_ShouldReturnTrue(self):
        validator = NotNullValidator(column_index=1)
        row = Row([1, "Bob", 25]) 
        
        result = validator.validate(row)
        assert result is True

    def test_Validate_WhenValueIsNull_ShouldThrow(self):
        validator = NotNullValidator(column_index=1)
        row = Row([2, None, 30]) 
        
        with pytest.raises(ConstraintViolationException):
            validator.validate(row)


class TestUniqueValidator:
    def test_Validate_WhenValueIsUnique_ShouldReturnTrue(self):
        validator = UniqueValidator(column_index=0)
        row1 = Row([100, "Alice"])
        row2 = Row([101, "Bob"])
        
        assert validator.validate(row1) is True
        assert validator.validate(row2) is True

    def test_Validate_WhenValueIsDuplicate_ShouldThrow(self):
        validator = UniqueValidator(column_index=0)
        row1 = Row([100, "Alice"])
        row2 = Row([100, "DuplicateID"])
        
        validator.validate(row1)
        
        with pytest.raises(ConstraintViolationException):
            validator.validate(row2)  
