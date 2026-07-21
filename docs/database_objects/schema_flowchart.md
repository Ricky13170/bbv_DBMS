# Schema Object: Internal Flowcharts

These flowcharts follow **Step 5** of our plan, showing the internal decision tree and logic for the core methods of `Schema`.

## 1. `AddTable(table)` Flowchart

```mermaid
flowchart TD
    Start([AddTable]) --> GetName[table_name = table.Name]
    GetName --> CheckName{Is table_name in _tables dictionary?}
    
    CheckName -- Yes --> ThrowErr[Raise DuplicateTableNameException]
    CheckName -- No --> Map["Store: _tables[table_name] = table"]
    Map --> Finish([Return success])
```

## 2. `GetTable(tableName)` Flowchart

```mermaid
flowchart TD
    Start([GetTable]) --> CheckName{Is tableName in _tables dictionary?}
    
    CheckName -- No --> ThrowErr[Raise TableNotFoundException]
    CheckName -- Yes --> Retrieve["Return _tables[tableName]"]
```
