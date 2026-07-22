from typing import Any

class Column:

    SUPPORTED_TYPES = {"int", "str", "float", "bool", "date", "bytes"}

    def __init__(self, name: str, data_type: str, is_nullable: bool = True):
        if not name or not name.strip():
            raise ValueError("Column name cannot be empty.")
        if data_type not in Column.SUPPORTED_TYPES:
            raise ValueError(f"Unsupported data type: '{data_type}'. "
                             f"Supported: {Column.SUPPORTED_TYPES}")
        self._name = name
        self._data_type = data_type
        self._is_nullable = is_nullable


    @property
    def name(self) -> str:
        return self._name

    @property
    def data_type(self) -> str:
        return self._data_type

    @property
    def is_nullable(self) -> bool:
        return self._is_nullable


    def validate_value(self, value: Any) -> bool:
        if value is None:
            return self._is_nullable

        type_mapping = {
            "int": int,
            "str": str,
            "float": float,
            "bool": bool,
            "bytes": bytes,
        }

        if self._data_type == "date":
            from datetime import date, datetime
            return isinstance(value, (date, datetime, str))

        expected_type = type_mapping.get(self._data_type)
        if expected_type:
            return isinstance(value, expected_type)
            
        return False


    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Column):
            return NotImplemented
        return (self._name == other._name
                and self._data_type == other._data_type
                and self._is_nullable == other._is_nullable)

    def __hash__(self) -> int:
        return hash((self._name, self._data_type, self._is_nullable))

    def __repr__(self) -> str:
        nullable = "NULL" if self._is_nullable else "NOT NULL"
        return f"Column({self._name!r}, {self._data_type!r}, {nullable})"
