import pytest
from unittest.mock import MagicMock
from src.database_objects.view import View

class TestView:

    def test_View_Init_ShouldStoreQuery(self):
        view = View("active_users", "SELECT * FROM users WHERE active = 1")
        assert view.name == "active_users"
        assert view.query_definition == "SELECT * FROM users WHERE active = 1"

    def test_View_Create_ShouldInitialize(self):
        view = View("active_users", "SELECT * FROM users")
        view.create()
            
    def test_View_Drop_ShouldCleanUp(self):
        view = View("active_users", "SELECT * FROM users")
        view.drop()

    def test_View_Resolve_ShouldCompileQuery(self):
        view = View("active_users", "SELECT * FROM users")
        mock_schema = MagicMock()
        # Red phase: expecting this to fail
        assert view.resolve(mock_schema) == "COMPILATION_MOCK"
