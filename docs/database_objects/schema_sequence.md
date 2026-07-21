# Schema Object: Sequence Diagrams

These diagrams follow **Step 4** of our plan, mapping out the interactions when manipulating a Schema object. 
In this Top-Down approach, `Schema` acts as an in-memory logical container holding `Table` objects.

## 1. AddTable Sequence

```mermaid
sequenceDiagram
    participant User as TestRunner
    participant Schema
    participant Table
    
    User->>Schema: AddTable(table)
    activate Schema
    
    Schema->>Table: get Name()
    Table-->>Schema: returns tableName
    
    Schema->>Schema: ContainsTable(tableName)
    
    alt exists == True
        Schema-->>User: Raise DuplicateTableNameException
    else exists == False
        Schema->>Schema: _tables[tableName] = table
        Schema-->>User: return void
    end
    deactivate Schema
```

## 2. RemoveTable Sequence

```mermaid
sequenceDiagram
    participant User as TestRunner
    participant Schema
    
    User->>Schema: RemoveTable(tableName)
    activate Schema
    
    Schema->>Schema: ContainsTable(tableName)
    
    alt exists == False
        Schema-->>User: Raise TableNotFoundException
    else exists == True
        Schema->>Schema: delete _tables[tableName]
        Schema-->>User: return void
    end
    deactivate Schema
```
