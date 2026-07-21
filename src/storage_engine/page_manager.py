from .file_manager import FileManager
import os

class PageID:
    def __init__(self, file_path: str, page_num: int):
        self.file_path = file_path
        self.page_num = page_num

class InvalidPageSizeException(Exception):
    pass

class CorruptedPageException(Exception):
    pass

class PageManager:
    PAGE_SIZE = 4096

    def __init__(self, file_manager: FileManager):
        self._file_manager = file_manager

    def read_page(self, page_id: PageID) -> bytes:
        handle = self._file_manager.open_file(page_id.file_path)
        offset = page_id.page_num * self.PAGE_SIZE
        data = self._file_manager.read_block(handle, offset, self.PAGE_SIZE)
        
        if len(data) != self.PAGE_SIZE:
            raise CorruptedPageException("Data read is smaller than PAGE_SIZE")
            
        return data

    def write_page(self, page_id: PageID, data: bytes) -> bool:
        if len(data) != self.PAGE_SIZE:
            raise InvalidPageSizeException(f"Data size must be {self.PAGE_SIZE} bytes")
            
        handle = self._file_manager.open_file(page_id.file_path)
        offset = page_id.page_num * self.PAGE_SIZE
        return self._file_manager.write_block(handle, offset, data)

    def allocate_page(self, file_path: str) -> PageID:
        if os.path.exists(file_path):
            file_size = os.path.getsize(file_path)
        else:
            file_size = 0
            
        new_page_num = file_size // self.PAGE_SIZE
        
        handle = self._file_manager.open_file(file_path)
        offset = new_page_num * self.PAGE_SIZE
        zero_buffer = b'\x00' * self.PAGE_SIZE
        
        self._file_manager.write_block(handle, offset, zero_buffer)
        
        return PageID(file_path, new_page_num)
