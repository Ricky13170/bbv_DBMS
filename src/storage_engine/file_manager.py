import os
from typing import Dict

class MaxOpenFilesExceededException(Exception):
    pass

class InvalidHandleException(Exception):
    pass

class FileInUseException(Exception):
    pass

class FileHandle:
    def __init__(self, fd: int, path: str):
        self.fd = fd
        self.path = path
        self.is_active = True

class FileManager:
    def __init__(self, max_open_files: int = 100):
        self._max_open_files = max_open_files
        self._current_open_count = 0
        self._active_handles: Dict[str, FileHandle] = {}

    def create_file(self, path: str) -> FileHandle:
        if os.path.exists(path):
            raise FileExistsError("File already exists")
        fd = os.open(path, os.O_CREAT | os.O_RDWR)
        handle = FileHandle(fd, path)
        self._active_handles[path] = handle
        self._current_open_count += 1
        return handle

    def open_file(self, path: str) -> FileHandle:
        if not os.path.exists(path):
            raise FileNotFoundError("File not found")
        if path in self._active_handles:
            return self._active_handles[path]
        if self._current_open_count >= self._max_open_files:
            raise MaxOpenFilesExceededException("Max open files exceeded")
        fd = os.open(path, os.O_RDWR)
        handle = FileHandle(fd, path)
        self._active_handles[path] = handle
        self._current_open_count += 1
        return handle

    def read_block(self, handle: FileHandle, offset: int, size: int) -> bytes:
        if not handle.is_active or handle.path not in self._active_handles:
            raise InvalidHandleException("Handle is closed or invalid")
        if offset < 0:
            raise ValueError("Offset cannot be negative")
        os.lseek(handle.fd, offset, os.SEEK_SET)
        data = os.read(handle.fd, size)
        return data

    def write_block(self, handle: FileHandle, offset: int, data: bytes) -> bool:
        if not handle.is_active or handle.path not in self._active_handles:
            raise InvalidHandleException("Handle is closed or invalid")
        if offset < 0:
            raise ValueError("Offset cannot be negative")
        os.lseek(handle.fd, offset, os.SEEK_SET)
        os.write(handle.fd, data)
        return True

    def close_file(self, handle: FileHandle) -> bool:
        if not handle.is_active or handle.path not in self._active_handles:
            raise InvalidHandleException("Handle is closed or invalid")
        os.close(handle.fd)
        handle.is_active = False
        del self._active_handles[handle.path]
        self._current_open_count -= 1
        return True

    def delete_file(self, path: str) -> bool:
        if path in self._active_handles and self._active_handles[path].is_active:
            raise FileInUseException("Cannot delete an open file")
        if os.path.exists(path):
            os.remove(path)
        return True

    def is_open(self, path: str) -> bool:
        return path in self._active_handles
