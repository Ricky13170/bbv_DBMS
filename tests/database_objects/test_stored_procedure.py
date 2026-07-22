import pytest
from src.database_objects.stored_procedure import StoredProcedure

class TestStoredProcedure:

    def test_StoredProcedure_Init_ShouldStoreBody(self):
        sp = StoredProcedure("clean_old_logs", "DELETE FROM logs WHERE created_at < '2020-01-01';")
        assert sp.name == "clean_old_logs"
        assert sp.body == "DELETE FROM logs WHERE created_at < '2020-01-01';"

    def test_StoredProcedure_Create_ShouldInitialize(self):
        sp = StoredProcedure("clean", "DELETE FROM logs;")
        sp.create()
            
    def test_StoredProcedure_Drop_ShouldCleanUp(self):
        sp = StoredProcedure("clean", "DELETE FROM logs;")
        sp.drop()

    def test_StoredProcedure_Execute_ShouldRunLogic(self):
        sp = StoredProcedure("calculate_payroll", "...")
        # Red phase: execution logic isn't wired yet
        sp.execute(employee_id=45)
