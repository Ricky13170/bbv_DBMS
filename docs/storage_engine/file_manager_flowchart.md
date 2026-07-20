# FileManager Internal Logic Flowcharts

These flowcharts describe the internal logic and decision trees for the core methods in `FileManager`. They serve as the foundation for defining our edge cases and `Given/When/Then` test cases in Step 6.

## 1. `open_file(path)` Flowchart

```mermaid
flowchart TD
    Start([Start: open_file]) --> CheckRegistered{Is file registered<br>in Catalog?}
    CheckRegistered -- No --> Error1[Raise FileNotRegisteredException]
    CheckRegistered -- Yes --> CheckOpen{Is file already<br>in active_handles?}
    CheckOpen -- Yes --> ReturnCache[Return cached FileHandle]
    CheckOpen -- No --> CheckLimit{open_count < MAX_OPEN?}
    CheckLimit -- No --> Error2[Raise MaxOpenFilesExceededException]
    CheckLimit -- Yes --> OSOpen[Call os.open(path)]
    OSOpen --> CreateHandle[Instantiate FileHandle with fd]
    CreateHandle --> AddCache[Store in active_handles dictionary]
    AddCache --> Increment[Increment open_count]
    Increment --> End([Return new FileHandle])
```

## 2. `read_block(file_handle, offset, size)` Flowchart

```mermaid
flowchart TD
    Start([Start: read_block]) --> CheckHandle{Is file_handle valid<br>& in active list?}
    CheckHandle -- No --> Error1[Raise InvalidHandleException]
    CheckHandle -- Yes --> CheckOffset{Is offset >= 0?}
    CheckOffset -- No --> Error2[Raise InvalidOffsetException]
    CheckOffset -- Yes --> OSLseek[Call os.lseek(fd, offset)]
    OSLseek --> CheckSeek{Seek Success?}
    CheckSeek -- No --> Error3[Raise IOError]
    CheckSeek -- Yes --> OSRead[Call os.read(fd, size)]
    OSRead --> Return([Return byte[] data])
```

## 3. `write_block(file_handle, offset, data)` Flowchart

```mermaid
flowchart TD
    Start([Start: write_block]) --> CheckHandle{Is file_handle valid<br>& in active list?}
    CheckHandle -- No --> Error1[Raise InvalidHandleException]
    CheckHandle -- Yes --> CheckOffset{Is offset >= 0?}
    CheckOffset -- No --> Error2[Raise InvalidOffsetException]
    CheckOffset -- Yes --> OSLseek[Call os.lseek(fd, offset)]
    OSLseek --> CheckSeek{Seek Success?}
    CheckSeek -- No --> Error3[Raise IOError]
    CheckSeek -- Yes --> OSWrite[Call os.write(fd, data)]
    OSWrite --> Return([Return bytes_written / True])
```

## 4. `close_file(file_handle)` Flowchart

```mermaid
flowchart TD
    Start([Start: close_file]) --> CheckHandle{Is file_handle valid<br>& in active list?}
    CheckHandle -- No --> Error1[Raise InvalidHandleException]
    CheckHandle -- Yes --> OSClose[Call os.close(fd)]
    OSClose --> RemoveCache[Remove from active_handles]
    RemoveCache --> Decrement[Decrement open_count]
    Decrement --> End([Return True])
```
