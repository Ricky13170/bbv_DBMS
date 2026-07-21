# PageManager Unit Test Sequences

These sequence diagrams define how `PageManager` interacts with the `FileManager` class during various page operations.

## 1. ReadPage Sequence
Illustrates how the system calculates the correct byte offset based on `PageID` and delegates to `FileManager`.

```mermaid
sequenceDiagram
    participant TestRunner as ReadPageTests
    participant PageManager
    participant FileManager
    
    TestRunner->>PageManager: read_page(page_id: PageID)
    activate PageManager
    
    %% Compute the target position
    PageManager->>PageManager: Calculate offset = page_id.page_num * PAGE_SIZE
    
    %% Forward request to FileManager
    PageManager->>FileManager: read_block(file_handle, offset, PAGE_SIZE)
    activate FileManager
    FileManager-->>PageManager: return byte[] data
    deactivate FileManager
    
    PageManager-->>TestRunner: return Page Object (bytes)
    deactivate PageManager
```

## 2. WritePage Sequence
Illustrates delegating page data to the correct file block.

```mermaid
sequenceDiagram
    participant TestRunner as WritePageTests
    participant PageManager
    participant FileManager
    
    TestRunner->>PageManager: write_page(page_id, data)
    activate PageManager
    
    PageManager->>PageManager: Validate len(data) == PAGE_SIZE
    
    alt Invalid Size
        PageManager-->>TestRunner: Raise InvalidPageSizeException
    else Valid Size
        PageManager->>PageManager: offset = page_id.page_num * PAGE_SIZE
        PageManager->>FileManager: write_block(file_handle, offset, data)
        FileManager-->>PageManager: return True
        PageManager-->>TestRunner: return True
    end
    deactivate PageManager
```

## 3. AllocatePage Sequence
Finding a page index and assigning it. (A simplistic append allocation approach).

```mermaid
sequenceDiagram
    participant TestRunner as AllocatePageTests
    participant PageManager
    participant FileManager
    
    TestRunner->>PageManager: allocate_page(file_path: String)
    activate PageManager
    
    %% We need file info to know how many pages exist
    %% In a real engine, we'd have a free space map, but for MVP we append
    PageManager->>FileManager: query file_size / page count (or mock internal logic)
    
    PageManager->>PageManager: Calculate new_page_num
    PageManager->>PageManager: Create zero-filled Page buffer
    
    PageManager->>FileManager: write_block(..., zero_buffer)
    FileManager-->>PageManager: return True
    
    PageManager-->>TestRunner: return new PageID
    deactivate PageManager
```
