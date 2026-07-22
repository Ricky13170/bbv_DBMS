from src.database_objects.database_object import DatabaseObject

class View(DatabaseObject):
    def __init__(self, name: str, query_definition: str):
        super().__init__(name)
        self.query_definition = query_definition

    def create(self) -> None:
        raise NotImplementedError()

    def drop(self) -> None:
        raise NotImplementedError()

    def resolve(self, schema) -> str:
        raise NotImplementedError()
