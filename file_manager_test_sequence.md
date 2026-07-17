# FileManager Unit Test Sequences

These sequence diagrams illustrate the execution flow during Unit Testing. They start from the Test Class (`CreateFileTests`, `OpenFileTests`, etc.), call the actual `FileManager` component, and show how `FileManager` interacts with Mocked dependencies (like the OS Layer or Mock Data Registry).

## 1. CreateFileTests Sequence
This tests the scenario where a new file is created successfully.

```mermaid
sequenceDiagram
    participant TestRunner as CreateFileTests
    participant FileManager
    participant MockOSWrapper

    TestRunner->>FileManager: create_file("db_data_1.dat", DATA)
    activate FileManager
    
    FileManager->>MockOSWrapper: os.path.exists("db_data_1.dat")
    MockOSWrapper-->>FileManager: return False (Mocked)
    
    FileManager->>MockOSWrapper: os.open(..., O_CREAT)
    MockOSWrapper-->>FileManager: return FileDescriptor (Mocked fd=3)
    
    FileManager->>FileManager: Allocate FileHandle(fd=3)
    FileManager-->>TestRunner: FileHandle Object
    deactivate FileManager
    
    TestRunner->>TestRunner: Assert Handle is Valid & fd == 3
```

## 2. OpenFileTests Sequence
This tests the scenario where an existing file is opened, enforcing the `max_open` limit.

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
        TestRunner->>TestRunner: Assert Handle Valid
    end
    deactivate FileManager
```

## 3. CloseFileTests Sequence
This tests releasing a handle and decrementing the open count.

```mermaid
sequenceDiagram
    participant TestRunner as CloseFileTests
    participant FileManager

    TestRunner->>FileManager: close_file(file_handle)
    activate FileManager
    
    FileManager->>FileManager: remove from active_handles cache
    FileManager->>FileManager: decrement open_count
    
    FileManager-->>TestRunner: return True (Success)
    deactivate FileManager
    
    TestRunner->>TestRunner: Assert handle in active_handles is False
    TestRunner->>FileManager: read_block(file_handle)
    FileManager-->>TestRunner: raise InvalidHandleException
    TestRunner->>TestRunner: Assert Exception Caught
```

## 4. DeleteFileTests Sequence
This tests deleting a file when it's closed, and failing to delete if it's currently open.

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
        FileManager-->>TestRunner: return True
        TestRunner->>TestRunner: Assert file removed from tracked lists
    end
    deactivate FileManager
```
