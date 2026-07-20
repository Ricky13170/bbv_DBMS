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
        raise NotImplementedError()

    def open_file(self, path: str) -> FileHandle:
        raise NotImplementedError()

    def read_block(self, handle: FileHandle, offset: int, size: int) -> bytes:
        raise NotImplementedError()

    def write_block(self, handle: FileHandle, offset: int, data: bytes) -> bool:
        raise NotImplementedError()

    def close_file(self, handle: FileHandle) -> bool:
        raise NotImplementedError()

    def delete_file(self, path: str) -> bool:
        raise NotImplementedError()

    def is_open(self, path: str) -> bool:
        return path in self._active_handles
