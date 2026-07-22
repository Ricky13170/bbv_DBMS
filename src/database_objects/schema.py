from typing import List, Optional
from src.database_objects.table import Table
from src.database_objects.view import View
from src.database_objects.sequence import Sequence
from src.database_objects.stored_procedure import StoredProcedure
from src.database_objects.database_object import DatabaseObject

class DuplicateObjectException(Exception): pass
class ObjectNotFoundException(Exception): pass
class DependencyViolationException(Exception): pass

class Schema(DatabaseObject):
    def __init__(self, name: str, owner: str = "admin"):
        super().__init__(name)
        self.owner = owner
        self._tables: List[Table] = []
        self._views: List[View] = []
        self._sequences: List[Sequence] = []
        self._procedures: List[StoredProcedure] = []

    def create(self) -> None:
        raise NotImplementedError()

    def drop(self) -> None:
        raise NotImplementedError()

    def add_table(self, table: Table) -> None:
        raise NotImplementedError()

    def get_table(self, table_name: str) -> Table:
        raise NotImplementedError()

    def drop_table(self, table_name: str) -> None:
        raise NotImplementedError()

    def rename_table(self, old_name: str, new_name: str) -> None:
        raise NotImplementedError()

    def list_all_tables(self) -> List[Table]:
        raise NotImplementedError()


    def add_view(self, view: View) -> None:
        raise NotImplementedError()

    def get_view(self, view_name: str) -> View:
        raise NotImplementedError()

    def drop_view(self, view_name: str) -> None:
        raise NotImplementedError()


    def add_sequence(self, sequence: Sequence) -> None:
        raise NotImplementedError()

    def get_sequence(self, sequence_name: str) -> Sequence:
        raise NotImplementedError()

    def drop_sequence(self, sequence_name: str) -> None:
        raise NotImplementedError()


    def add_procedure(self, procedure: StoredProcedure) -> None:
        raise NotImplementedError()

    def get_procedure(self, procedure_name: str) -> StoredProcedure:
        raise NotImplementedError()

    def drop_procedure(self, procedure_name: str) -> None:
        raise NotImplementedError()
