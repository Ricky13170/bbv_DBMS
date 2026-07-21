from .schema import Schema
from typing import Dict

class CatalogManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CatalogManager, cls).__new__(cls)
            cls._instance._schemas = {}
        return cls._instance

    def __init__(self):
        pass

    def get_schema(self, name: str) -> Schema:
        if name not in self._schemas:
            raise KeyError(f"Schema '{name}' not found.")
        return self._schemas[name]

    def add_schema(self, schema: Schema) -> None:
        if schema.name in self._schemas:
            raise ValueError(f"Schema '{schema.name}' already exists.")
        self._schemas[schema.name] = schema
