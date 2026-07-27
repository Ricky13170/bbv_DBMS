import pytest
from src.database_objects.database_catalog import RelationalDatabaseCatalog, DatabaseExistsException, DatabaseNotFoundException

class TestDatabaseCatalog:
    def setup_method(self):
        self.catalog = RelationalDatabaseCatalog()

    def test_CreateDatabase_WithValidName_ShouldReturnDatabaseInstance(self):
        from src.database_objects.database import IDatabase
        db = self.catalog.create_database("Tiki")
        assert db is not None
        assert db.name == "Tiki"
        assert isinstance(db, IDatabase)

    def test_CreateDatabase_WithDuplicateName_ShouldRaiseException(self):
        self.catalog.create_database("Tiki")
        with pytest.raises(DatabaseExistsException):
            self.catalog.create_database("Tiki")

    def test_CreateDatabase_WithEmptyName_ShouldRaiseValueError(self):
        with pytest.raises(ValueError):
            self.catalog.create_database("")

    def test_DropDatabase_ShouldRemoveFromCatalog(self):
        self.catalog.create_database("Shopee")
        self.catalog.drop_database("Shopee")
        with pytest.raises(DatabaseNotFoundException):
            self.catalog.get_database("Shopee")

    def test_GetDatabase_WhenNotExists_ShouldRaiseDatabaseNotFoundException(self):
        with pytest.raises(DatabaseNotFoundException):
            self.catalog.get_database("GhostDB")
