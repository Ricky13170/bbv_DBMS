import pytest
import os
from src.storage_engine.file_manager import (
    FileManager, 
    FileHandle,
    MaxOpenFilesExceededException,
    InvalidHandleException,
    FileInUseException
)

class TestCreateFile:
    def test_CreateFile_WhenPathIsValid_ShouldCreateAndReturnHandle(self, mocker):
        # Mock OS layer
        mocker.patch('os.path.exists', return_value=False)
        mocker.patch('os.open', return_value=3)
        manager = FileManager()
        
        handle = manager.create_file("test.dat")
        
        assert handle is not None
        assert handle.fd == 3
        assert handle.path == "test.dat"
        assert manager.is_open("test.dat")
        assert handle.is_active

    def test_CreateFile_WhenFileAlreadyExists_ShouldThrow(self, mocker):
        mocker.patch('os.path.exists', return_value=True)
        manager = FileManager()
        
        with pytest.raises(FileExistsError):
            manager.create_file("test.dat")

class TestOpenFile:
    def test_OpenFile_WhenBelowLimit_ShouldReturnHandle(self, mocker):
        mocker.patch('os.path.exists', return_value=True)
        mocker.patch('os.open', return_value=4)
        manager = FileManager(max_open_files=10)
        
        handle = manager.open_file("test2.dat")
        
        assert handle.fd == 4
        assert handle.path == "test2.dat"
        assert manager.is_open("test2.dat")

    def test_OpenFile_WhenAlreadyOpen_ShouldReturnCachedHandle(self, mocker):
        mocker.patch('os.path.exists', return_value=True)
        mock_open = mocker.patch('os.open', side_effect=[5, 6])
        manager = FileManager()
        
        handle1 = manager.open_file("test3.dat")
        handle2 = manager.open_file("test3.dat")
        
        # Expected behavior: os.open called only once, handles are exactly the same
        assert mock_open.call_count == 1
        assert handle1 is handle2

    def test_OpenFile_WhenAboveLimit_ShouldThrow(self, mocker):
        mocker.patch('os.path.exists', return_value=True)
        mocker.patch('os.open', return_value=99)
        manager = FileManager(max_open_files=1) # Limit is 1
        
        manager.open_file("first.dat") # First one ok
        
        with pytest.raises(MaxOpenFilesExceededException):
            manager.open_file("second.dat") # Second one throws

    def test_OpenFile_WhenFileDoesNotExist_ShouldThrow(self, mocker):
        mocker.patch('os.path.exists', return_value=False)
        manager = FileManager()
        
        with pytest.raises(FileNotFoundError):
            manager.open_file("not_found.dat")

class TestReadBlock:
    def test_ReadBlock_WhenHandleIsValid_ShouldReturnData(self, mocker):
        mocker.patch('os.lseek')
        mocker.patch('os.read', return_value=b"test data block")
        
        manager = FileManager()
        # Create a mock active handle inside the manager (bypassing open for isolated test)
        handle = FileHandle(10, "read.dat")
        manager._active_handles["read.dat"] = handle
        
        data = manager.read_block(handle, offset=0, size=1024)
        
        assert data == b"test data block"

    def test_ReadBlock_WhenOffsetIsOutOfBounds_ShouldThrow(self, mocker):
        manager = FileManager()
        handle = FileHandle(10, "read.dat")
        manager._active_handles["read.dat"] = handle
        
        with pytest.raises(ValueError):
            manager.read_block(handle, offset=-1, size=1024)

    def test_ReadBlock_WhenHandleIsClosed_ShouldThrow(self):
        manager = FileManager()
        handle = FileHandle(99, "closed.dat")
        handle.is_active = False # Manual test simulation
        
        with pytest.raises(InvalidHandleException):
            manager.read_block(handle, offset=0, size=1024)

class TestWriteBlock:
    def test_WriteBlock_WhenDataIsValid_ShouldWriteAndReturnTrue(self, mocker):
        mocker.patch('os.lseek')
        mock_write = mocker.patch('os.write', return_value=12)
        
        manager = FileManager()
        handle = FileHandle(11, "write.dat")
        manager._active_handles["write.dat"] = handle
        
        result = manager.write_block(handle, offset=4096, data=b"hello data")
        
        assert result is True
        mock_write.assert_called_once_with(11, b"hello data")

    def test_WriteBlock_WhenHandleIsClosed_ShouldThrow(self):
        manager = FileManager()
        handle = FileHandle(11, "closed_w.dat")
        handle.is_active = False 
        
        with pytest.raises(InvalidHandleException):
            manager.write_block(handle, offset=0, data=b"fail")

class TestCloseFile:
    def test_CloseFile_WhenHandleIsValid_ShouldCloseAndDecrementCount(self, mocker):
        mock_close = mocker.patch('os.close')
        
        manager = FileManager()
        handle = FileHandle(20, "close.dat")
        manager._active_handles["close.dat"] = handle
        manager._current_open_count = 1
        
        result = manager.close_file(handle)
        
        assert result is True
        assert not handle.is_active
        assert "close.dat" not in manager._active_handles
        assert manager._current_open_count == 0
        mock_close.assert_called_once_with(20)

    def test_CloseFile_WhenHandleIsAlreadyClosed_ShouldThrow(self):
        manager = FileManager()
        handle = FileHandle(20, "already_close.dat")
        handle.is_active = False
        
        with pytest.raises(InvalidHandleException):
            manager.close_file(handle)

class TestDeleteFile:
    def test_DeleteFile_WhenFileIsClosed_ShouldRemoveFile(self, mocker):
        mock_remove = mocker.patch('os.remove')
        mocker.patch('os.path.exists', return_value=True)
        manager = FileManager()
        
        result = manager.delete_file("delete_me.dat")
        
        assert result is True
        mock_remove.assert_called_once_with("delete_me.dat")

    def test_DeleteFile_WhenFileIsOpen_ShouldThrow(self, mocker):
        manager = FileManager()
        handle = FileHandle(30, "open_file.dat")
        manager._active_handles["open_file.dat"] = handle 
        
        with pytest.raises(FileInUseException):
            manager.delete_file("open_file.dat")
