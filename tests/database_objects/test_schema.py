import pytest
from src.database_objects.schema import Schema, DuplicateObjectException, ObjectNotFoundException
from src.database_objects.table import Table
from src.database_objects.view import View
from src.database_objects.sequence import Sequence
from src.database_objects.stored_procedure import StoredProcedure

class TestSchemaTables:
    def test_CreateTable_ShouldStoreInSchema(self):
        schema = Schema("StudentSchema", "admin")
        table = Table("users")
        schema.add_table(table)
        retrieved = schema.get_table("users")
        assert retrieved is not None
        assert retrieved.name == "users"

    def test_DropTable_ShouldRemoveFromSchema(self):
        schema = Schema("StudentSchema", "admin")
        table = Table("users")
        schema.add_table(table)
        schema.drop_table("users")
        with pytest.raises(ObjectNotFoundException):
            schema.get_table("users")

    def test_RenameTable_ShouldUpdateInternalReferences(self):
        schema = Schema("StudentSchema", "admin")
        table = Table("users")
        schema.add_table(table)
        schema.rename_table("users", "customers")
        retrieved = schema.get_table("customers")
        assert retrieved is not None
        assert retrieved.name == "customers"
        with pytest.raises(ObjectNotFoundException):
            schema.get_table("users")

    def test_ListAllTables_ShouldReturnAllInsertedTables(self):
        schema = Schema("StudentSchema", "admin")
        schema.add_table(Table("users"))
        schema.add_table(Table("orders"))
        tables = schema.list_all_tables()
        assert len(tables) == 2

    def test_RejectDuplicateTableName_ShouldThrow(self):
        schema = Schema("StudentSchema", "admin")
        schema.add_table(Table("users"))
        with pytest.raises(DuplicateObjectException):
            schema.add_table(Table("users"))

    def test_RejectUnknownTable_ForDrop_ShouldThrow(self):
        schema = Schema("StudentSchema", "admin")
        with pytest.raises(ObjectNotFoundException):
            schema.drop_table("unknown-tbl")

class TestSchemaViews:
    def test_CreateView_ShouldStoreInSchema(self):
        schema = Schema("StudentSchema", "admin")
        view = View("view-001", "SELECT * FROM users")
        schema.add_view(view)
        assert schema.get_view("view-001") is not None

    def test_DropView_ShouldRemoveFromSchema(self):
        schema = Schema("StudentSchema")
        view = View("view-001", "SELECT * FROM users")
        schema.add_view(view)
        schema.drop_view("view-001")
        with pytest.raises(ObjectNotFoundException):
            schema.get_view("view-001")

class TestSchemaProcedures:
    def test_CreateProcedure_ShouldStoreInSchema(self):
        schema = Schema("StudentSchema")
        proc = StoredProcedure("proc-001", "END;")
        schema.add_procedure(proc)
        assert schema.get_procedure("proc-001") is not None

    def test_DropProcedure_ShouldRemoveFromSchema(self):
        schema = Schema("StudentSchema")
        proc = StoredProcedure("proc-001", "END;")
        schema.add_procedure(proc)
        schema.drop_procedure("proc-001")
        with pytest.raises(ObjectNotFoundException):
            schema.get_procedure("proc-001")

class TestSchemaSequences:
    def test_CreateSequence_ShouldStoreInSchema(self):
        schema = Schema("StudentSchema")
        seq = Sequence("seq-001")
        schema.add_sequence(seq)
        assert schema.get_sequence("seq-001") is not None

    def test_DropSequence_ShouldRemoveFromSchema(self):
        schema = Schema("StudentSchema")
        schema.add_sequence(Sequence("seq-001"))
        schema.drop_sequence("seq-001")
        with pytest.raises(ObjectNotFoundException):
            schema.get_sequence("seq-001")
