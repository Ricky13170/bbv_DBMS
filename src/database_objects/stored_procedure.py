from typing import List, Any

from src.database_objects.database_object import DatabaseObject

class StoredProcedure(DatabaseObject):
    def __init__(self, name: str, body: str):
        super().__init__(name)
        self.body = body

    def create(self) -> None:
        raise NotImplementedError()

    def drop(self) -> None:
        raise NotImplementedError()

    def execute(self, *args, **kwargs) -> Any:
        raise NotImplementedError()
