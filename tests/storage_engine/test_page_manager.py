import pytest
from src.storage_engine.file_manager import FileManager, FileHandle, InvalidHandleException
from src.storage_engine.page_manager import (
    PageManager, PageID, InvalidPageSizeException, CorruptedPageException
)

class TestReadPage:
    def test_ReadPage_WhenValid_ShouldMapOffsetAndCallFileManager(self, mocker):
        mock_file_manager = mocker.Mock(spec=FileManager)
        handle = FileHandle(3, "test.dat")
        mock_file_manager.open_file.return_value = handle
        mock_file_manager.read_block.return_value = b'x' * 4096

        page_manager = PageManager(mock_file_manager)
        page_id = PageID("test.dat", 2)
        
        data = page_manager.read_page(page_id)
        
        assert data == b'x' * 4096
        # Expected offset calculations: 2 * 4096 = 8192
        mock_file_manager.open_file.assert_called_once_with("test.dat")
        mock_file_manager.read_block.assert_called_once_with(handle, 8192, 4096)

    def test_ReadPage_WhenDataIsTruncated_ShouldThrow(self, mocker):
        mock_file_manager = mocker.Mock(spec=FileManager)
        handle = FileHandle(3, "test.dat")
        mock_file_manager.open_file.return_value = handle
        mock_file_manager.read_block.return_value = b'x' * 1024 # Mocking a corruption (too short)

        page_manager = PageManager(mock_file_manager)
        page_id = PageID("test.dat", 0)
        
        with pytest.raises(CorruptedPageException):
            page_manager.read_page(page_id)

class TestWritePage:
    def test_WritePage_WhenSizeIsExactlyPageSize_ShouldCallFileManager(self, mocker):
        mock_file_manager = mocker.Mock(spec=FileManager)
        handle = FileHandle(3, "write.dat")
        mock_file_manager.open_file.return_value = handle
        mock_file_manager.write_block.return_value = True

        page_manager = PageManager(mock_file_manager)
        page_id = PageID("write.dat", 1)
        data = b'w' * 4096
        
        result = page_manager.write_page(page_id, data)
        
        assert result is True
        mock_file_manager.write_block.assert_called_once_with(handle, 4096, data)

    def test_WritePage_WhenSizeMismatch_ShouldThrow(self, mocker):
        page_manager = PageManager(None) # Validation happens before FileManager is called
        page_id = PageID("write.dat", 1)
        
        with pytest.raises(InvalidPageSizeException):
            page_manager.write_page(page_id, b'short')

class TestAllocatePage:
    def test_AllocatePage_WhenCalled_ShouldAppendZeroBufferAndReturnID(self, mocker):
        # We mock os.path.getsize to fake that the file has 8192 bytes (2 pages)
        mocker.patch('os.path.getsize', return_value=8192)
        mocker.patch('os.path.exists', return_value=True)
        
        mock_file_manager = mocker.Mock(spec=FileManager)
        handle = FileHandle(4, "new.dat")
        mock_file_manager.open_file.return_value = handle
        mock_file_manager.write_block.return_value = True
        
        page_manager = PageManager(mock_file_manager)
        
        new_page_id = page_manager.allocate_page("new.dat")
        
        assert new_page_id.file_path == "new.dat"
        assert new_page_id.page_num == 2 # The new page should have index 2
        
        # Zero-filled buffer should be written
        expected_buffer = b'\x00' * 4096
        mock_file_manager.write_block.assert_called_once_with(handle, 8192, expected_buffer)
