# PageManager Test Cases & Detailed Contracts

Based on the Sequence logic, these are the test cases driving our TDD.

## 1. Unit Test Cases (Flowchart)

```mermaid
flowchart LR
    Subsystem[Storage Engine] --> PageManager
    
    %% Read Page Scenarios
    PageManager --> ReadPage_WhenValid_ShouldMapOffsetAndCallFileManager
    PageManager --> ReadPage_WhenFileNotOpen_ShouldThrow
    PageManager --> ReadPage_WhenDataIsTruncated_ShouldThrow
    
    %% Write Page Scenarios
    PageManager --> WritePage_WhenSizeIsExactlyPageSize_ShouldCallFileManager
    PageManager --> WritePage_WhenSizeMismatch_ShouldThrow
    
    %% Allocate Page Scenarios
    PageManager --> AllocatePage_WhenCalled_ShouldAppendZeroBufferAndReturnID
```

## 2. Derived Method Contracts (Detail Class Diagram)

```mermaid
classDiagram
    direction TB
    
    class PageID {
        +string FilePath
        +int PageNum
    }

    class PageManager {
        -FileManager _fileManager
        -int PAGE_SIZE (const: 4096)
        
        +ReadPage(PageID pageId) byte[]
        +WritePage(PageID pageId, byte[] data) bool
        +AllocatePage(string filePath) PageID
    }

    class InvalidPageSizeException
    class CorruptedPageException

    PageManager *-- PageID : uses
    PageManager --> InvalidPageSizeException : throws
    PageManager --> CorruptedPageException : throws
```
