from src.database_objects.database import Database

class DatabaseExistsException(Exception): pass
class DatabaseNotFoundException(Exception): pass

class DatabaseCatalog:
    def __init__(self):
        self._databases = {}

    def create_database(self, name: str) -> Database:
        raise NotImplementedError()

    def drop_database(self, name: str) -> None:
        raise NotImplementedError()

    def get_database(self, name: str) -> Database:
        raise NotImplementedError()
