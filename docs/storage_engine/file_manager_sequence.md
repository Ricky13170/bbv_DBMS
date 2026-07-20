# FileManager Unit Test Sequences

These sequence diagrams illustrate the execution flow during Unit Testing for the `FileManager` class. By following a Test-Driven Development (TDD) approach, these diagrams show how the `TestRunner` asserts behavior and how `FileManager` interacts with mocked dependencies (like `MockOSWrapper` or `MockRegistry`).

## 1. CreateFileTests Sequence
This tests creating a new database file.

```mermaid
sequenceDiagram
    participant TestRunner as CreateFileTests
    participant FileManager
    participant MockOSWrapper

    TestRunner->>FileManager: create_file("db_data_1.dat")
    activate FileManager
    
    FileManager->>MockOSWrapper: os.path.exists("db_data_1.dat")
    MockOSWrapper-->>FileManager: return False (Mocked)
    
    FileManager->>MockOSWrapper: os.open("db_data_1.dat", O_CREAT)
    MockOSWrapper-->>FileManager: return FileDescriptor (Mocked fd=3)
    
    FileManager->>FileManager: Allocate FileHandle(fd=3)
    FileManager-->>TestRunner: FileHandle Object
    deactivate FileManager
    
    TestRunner->>TestRunner: Assert Handle is Valid & fd == 3
```

## 2. OpenFileTests Sequence
This tests opening an existing file and enforcing a `max_open_files` limit.

```mermaid
sequenceDiagram
    participant TestRunner as OpenFileTests
    participant FileManager
    participant MockRegistry

    TestRunner->>FileManager: open_file("db_data_1.dat")
    activate FileManager
    
    FileManager->>MockRegistry: is_file_registered("db_data_1.dat")
    MockRegistry-->>FileManager: return True
    
    FileManager->>FileManager: check open_files_count < max_open
    
    alt Over limit
        FileManager-->>TestRunner: raise MaxOpenFilesExceededException
        TestRunner->>TestRunner: Assert Exception Caught
    else Within limit
        FileManager->>FileManager: create and cache FileHandle
        FileManager-->>TestRunner: FileHandle Object
        TestRunner->>TestRunner: Assert Handle Valid & in cache
    end
    deactivate FileManager
```

## 3. ReadBlockTests Sequence
This tests reading a specific block of data (page) from an open file.

```mermaid
sequenceDiagram
    participant TestRunner as ReadBlockTests
    participant FileManager
    participant MockOSWrapper

    TestRunner->>FileManager: read_block(file_handle, offset=4096, size=4096)
    activate FileManager
    
    FileManager->>FileManager: validate file_handle is active
    
    FileManager->>MockOSWrapper: os.lseek(file_handle.fd, offset)
    MockOSWrapper-->>FileManager: Success (Mocked)
    
    FileManager->>MockOSWrapper: os.read(file_handle.fd, size)
    MockOSWrapper-->>FileManager: return byte[] data (Mocked)
    
    FileManager-->>TestRunner: return byte[] data
    deactivate FileManager
    
    TestRunner->>TestRunner: Assert returned data matches expected bytes
```

## 4. WriteBlockTests Sequence
This tests writing a block of bytes (a page) to an open file.

```mermaid
sequenceDiagram
    participant TestRunner as WriteBlockTests
    participant FileManager
    participant MockOSWrapper

    TestRunner->>FileManager: write_block(file_handle, offset=4096, data)
    activate FileManager
    
    FileManager->>FileManager: validate file_handle is active
    
    FileManager->>MockOSWrapper: os.lseek(file_handle.fd, offset)
    MockOSWrapper-->>FileManager: Success (Mocked)
    
    FileManager->>MockOSWrapper: os.write(file_handle.fd, data)
    MockOSWrapper-->>FileManager: return bytes_written (Mocked)
    
    FileManager-->>TestRunner: return True (Success)
    deactivate FileManager
    
    TestRunner->>TestRunner: Assert True is returned
```

## 5. CloseFileTests Sequence
This tests releasing a handle and ensuring the file can no longer be read.

```mermaid
sequenceDiagram
    participant TestRunner as CloseFileTests
    participant FileManager
    participant MockOSWrapper

    TestRunner->>FileManager: close_file(file_handle)
    activate FileManager
    
    FileManager->>MockOSWrapper: os.close(file_handle.fd)
    MockOSWrapper-->>FileManager: Success (Mocked)
    
    FileManager->>FileManager: remove from active_handles cache
    FileManager->>FileManager: decrement open_count
    
    FileManager-->>TestRunner: return True (Success)
    deactivate FileManager
    
    TestRunner->>TestRunner: Assert file_handle is properly invalidated
    
    %% Verify attempting a read on closed handle fails
    TestRunner->>FileManager: read_block(file_handle, offset, size)
    FileManager-->>TestRunner: raise InvalidHandleException
    TestRunner->>TestRunner: Assert Exception Caught
```

## 6. DeleteFileTests Sequence
This tests deleting a file, ensuring it fails if the file is currently active/open.

```mermaid
sequenceDiagram
    participant TestRunner as DeleteFileTests
    participant FileManager
    participant MockOSWrapper

    TestRunner->>FileManager: delete_file("db_data_1.dat")
    activate FileManager
    
    FileManager->>FileManager: check is_open("db_data_1.dat")
    
    alt File is Open
        FileManager-->>TestRunner: raise FileInUseException
        TestRunner->>TestRunner: Assert Exception Caught
    else File is Closed
        FileManager->>MockOSWrapper: os.remove("db_data_1.dat")
        MockOSWrapper-->>FileManager: Success (Mocked)
        FileManager-->>TestRunner: return True (Success)
        TestRunner->>TestRunner: Assert file is removed from registry
    end
    deactivate FileManager
```
