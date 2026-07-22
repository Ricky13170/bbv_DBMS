from src.database_objects.schema import Schema

class CatalogManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CatalogManager, cls).__new__(cls)
            cls._instance._schemas = {}
        return cls._instance

    def get_schema(self, name: str) -> Schema:
        raise NotImplementedError()

    def add_schema(self, schema: Schema) -> None:
        raise NotImplementedError()

    def remove_schema(self, name: str) -> None:
        raise NotImplementedError()
