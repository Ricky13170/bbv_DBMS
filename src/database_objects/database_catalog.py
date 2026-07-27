from abc import ABC, abstractmethod
from src.database_objects.database import IDatabase, RelationalDatabase

class DatabaseExistsException(Exception): pass
class DatabaseNotFoundException(Exception): pass

class IDatabaseCatalog(ABC):
    """Abstract Creator"""
    @abstractmethod
    def create_database(self, name: str) -> IDatabase: pass
    
    @abstractmethod
    def drop_database(self, name: str) -> None: pass
    
    @abstractmethod
    def get_database(self, name: str) -> IDatabase: pass

class RelationalDatabaseCatalog(IDatabaseCatalog):
    """Concrete Creator"""
    def __init__(self):
        self._databases = {}

    def create_database(self, name: str) -> IDatabase:
        raise NotImplementedError()

    def drop_database(self, name: str) -> None:
        raise NotImplementedError()

    def get_database(self, name: str) -> IDatabase:
        raise NotImplementedError()
