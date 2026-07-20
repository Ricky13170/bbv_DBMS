# FileManager Test Cases & Detailed Contracts

This document combines **Step 6 (Test Case Flowchart)** and **Step 8 (Detailed Class Diagram)** for the `FileManager` class. It uses the `Method_Condition_Result` naming convention adapted from Behavior-Driven Development (BDD).

## 1. Unit Test Cases (Flowchart)

This diagram acts as a visual checklist for all the scenarios that the `FileManager` Unit Tests must cover.

```mermaid
flowchart LR
    Subsystem[Storage Engine] --> FileManager
    
    %% Create File Scenarios
    FileManager --> CreateFile_WhenPathIsValid_ShouldCreateAndReturnHandle
    FileManager --> CreateFile_WhenFileAlreadyExists_ShouldThrow
    FileManager --> CreateFile_WhenPathIsInvalid_ShouldThrow
    
    %% Open File Scenarios
    FileManager --> OpenFile_WhenBelowLimit_ShouldReturnHandle
    FileManager --> OpenFile_WhenAboveLimit_ShouldThrow
    FileManager --> OpenFile_WhenFileDoesNotExist_ShouldThrow
    
    %% Read Block Scenarios
    FileManager --> ReadBlock_WhenHandleIsValid_ShouldReturnData
    FileManager --> ReadBlock_WhenOffsetIsOutOfBounds_ShouldThrow
    FileManager --> ReadBlock_WhenHandleIsClosed_ShouldThrow
    
    %% Write Block Scenarios
    FileManager --> WriteBlock_WhenDataIsValid_ShouldWriteAndReturnTrue
    FileManager --> WriteBlock_WhenHandleIsClosed_ShouldThrow
    FileManager --> WriteBlock_WhenDiskIsFull_ShouldThrow
    
    %% Close File Scenarios
    FileManager --> CloseFile_WhenHandleIsValid_ShouldCloseAndDecrementCount
    FileManager --> CloseFile_WhenHandleIsAlreadyClosed_ShouldThrow
    
    %% Delete File Scenarios
    FileManager --> DeleteFile_WhenFileIsClosed_ShouldRemoveFile
    FileManager --> DeleteFile_WhenFileIsOpen_ShouldThrow
    FileManager --> DeleteFile_WhenFileDoesNotExist_ShouldThrow
```

## 2. Derived Method Contracts (Detail Class Diagram)

Based on the test scenarios derived above, we can firmly establish the Interface and Data Types (Contracts) needed for `FileManager` and its associated objects (like exceptions and models).

```mermaid
classDiagram
    direction TB
    
    class FileManager {
        -int _maxOpenFiles
        -int _currentOpenCount
        -Dictionary~string, FileHandle~ _activeHandles
        
        +CreateFile(string path) FileHandle
        +OpenFile(string path) FileHandle
        +ReadBlock(FileHandle handle, int offset, int size) byte[]
        +WriteBlock(FileHandle handle, int offset, byte[] data) bool
        +CloseFile(FileHandle handle) bool
        +DeleteFile(string path) bool
        +IsOpen(string path) bool
    }

    class FileHandle {
        +int FileDescriptor (FD)
        +string Path
        +bool IsActive
    }

    %% Exceptions clearly identified from the Test rules
    class IOException {
        +string Message
    }
    class MaxOpenFilesExceededException
    class InvalidHandleException
    class FileInUseException

    %% Relationships
    FileManager *-- FileHandle : "Creates & manages"
    IOException <|-- MaxOpenFilesExceededException
    IOException <|-- InvalidHandleException
    IOException <|-- FileInUseException

    %% Dependencies indicating the FileManager throws them
    FileManager ..> MaxOpenFilesExceededException : throws
    FileManager ..> InvalidHandleException : throws
    FileManager ..> FileInUseException : throws
```
