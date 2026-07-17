# High-Level Class Diagram: Storage Engine

This diagram illustrates the internal components of the **Storage Engine** subsystem.

```mermaid
classDiagram
    direction TB

    %% ==========================================
    %% STORAGE ENGINE SUBSYSTEM
    %% ==========================================
    namespace StorageEngine {
        class StorageEngine {
            +initialize()
            +shutdown()
        }
        class RecordManager {
            +read_record(id: RecordID) Record
            +insert_record(record: Record) RecordID
            +update_record(id: RecordID, record: Record) bool
            +delete_record(id: RecordID) bool
        }
        class IndexManager {
            +search(key: Key) RecordID
            +insert(key: Key, id: RecordID)
            +delete(key: Key)
        }
        class BTree {
            +root: Node
            +split()
            +merge()
        }
        class BufferPool {
            +fetch_page(page_id: PageID) Page
            +flush_page(page_id: PageID)
        }
        class PageManager {
            +allocate_page() PageID
            +free_page(page_id: PageID)
            +read_page(page_id: PageID) byte[]
            +write_page(page_id: PageID, data: byte[])
        }
        class FileManager {
            +open_file(path: String) FileHandle
            +read_block(handle: FileHandle, offset: int) byte[]
            +write_block(handle: FileHandle, offset: int, data: byte[])
        }
        class StorageAllocator {
            +allocate_extent() Extent
            +release_extent(extent: Extent)
        }
    }

    %% ==========================================
    %% INTERNAL RELATIONSHIPS
    %% ==========================================
    StorageEngine *-- RecordManager
    StorageEngine *-- IndexManager
    StorageEngine *-- BufferPool
    
    IndexManager *-- BTree
    RecordManager --> BufferPool : requests pages
    IndexManager --> BufferPool : requests index pages
    
    BufferPool --> PageManager : manages memory for
    PageManager --> FileManager : translates pages to blocks
    FileManager --> StorageAllocator : uses space on disk
```