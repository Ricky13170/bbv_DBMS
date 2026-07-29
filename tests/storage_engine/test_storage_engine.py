import pytest
from unittest.mock import patch, MagicMock

from src.storage_engine import (
    StorageEngine,
    EngineStatus,
    StorageEngineException,
    FileManager,
    PageManager,
    BufferPool,
    StorageAllocator
)

class TestStorageEngine:

    def setup_method(self):
        """Called before every test method."""
        self.engine = StorageEngine()
        # Reset the Singleton for StorageAllocator to prevent state leakage between tests
        StorageAllocator._instance = None

    def teardown_method(self):
        """Called after every test method."""
        if self.engine.get_engine_status() == EngineStatus.RUNNING:
            self.engine.shutdown()
        StorageAllocator._instance = None


    def test_initial_state_is_stopped(self):
        """Test that the engine is initialised in a STOPPED state with no active subsystems."""
        assert self.engine.get_engine_status() == EngineStatus.STOPPED
        assert self.engine.file_manager is None
        assert self.engine.page_manager is None
        assert self.engine.buffer_pool is None
        assert self.engine.storage_allocator is None

    
    def test_initialize_boots_all_subsystems_successfully(self):
        """Test that calling initialize() properly instantiates all subsystems and sets state to RUNNING."""
        self.engine.initialize(max_open_files=50, buffer_capacity=128, total_pages=512)
        
        assert self.engine.get_engine_status() == EngineStatus.RUNNING
        
        # Verify all subsystems are instantiated
        assert isinstance(self.engine.file_manager, FileManager)
        assert isinstance(self.engine.page_manager, PageManager)
        assert isinstance(self.engine.buffer_pool, BufferPool)
        assert isinstance(self.engine.storage_allocator, StorageAllocator)


    def test_initialize_twice_is_idempotent(self):
        """Test that calling initialize() a second time does not re-instantiate subsystems."""
        self.engine.initialize()
        original_buffer_pool = self.engine.buffer_pool
        
        # Call again
        self.engine.initialize()
        
        assert self.engine.get_engine_status() == EngineStatus.RUNNING
        # Ensure it wasn't overwritten
        assert self.engine.buffer_pool is original_buffer_pool


    def test_shutdown_cleans_up_subsystems(self):
        """Test that shutdown() drops all subsystem references and reverts to STOPPED state."""
        self.engine.initialize()
        assert self.engine.get_engine_status() == EngineStatus.RUNNING
        
        self.engine.shutdown()
        
        assert self.engine.get_engine_status() == EngineStatus.STOPPED
        assert self.engine.file_manager is None
        assert self.engine.page_manager is None
        assert self.engine.buffer_pool is None


    def test_shutdown_twice_is_idempotent(self):
        """Test that calling shutdown() on an already stopped engine does nothing."""
        assert self.engine.get_engine_status() == EngineStatus.STOPPED
        
        # Should not throw any exceptions
        self.engine.shutdown()
        assert self.engine.get_engine_status() == EngineStatus.STOPPED


    @patch("src.storage_engine.storage_engine.FileManager")
    def test_initialize_failure_rolls_back_to_error_state(self, mock_file_manager):
        """
        Test that if any subsystem fails to boot (e.g. FileManager raises IOError),
        the Facade catches it, sets status to ERROR, and raises StorageEngineException.
        """
        # Mock FileManager to simulate an OS-level initialization failure
        mock_file_manager.side_effect = Exception("OS level permission denied!")
        
        with pytest.raises(StorageEngineException) as exc_info:
            self.engine.initialize()
            
        assert "Failed to initialize engine" in str(exc_info.value)
        assert "permission denied" in str(exc_info.value)
        assert self.engine.get_engine_status() == EngineStatus.ERROR
        
        # Subsystems should remain None
        assert self.engine.page_manager is None
        assert self.engine.buffer_pool is None
