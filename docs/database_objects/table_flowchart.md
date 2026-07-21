# Table Object: Internal Flowcharts

These flowcharts outline the internal decision tree and logic for the core methods of `Table`.

## 1. `AddColumn(column)` Flowchart

```mermaid
flowchart TD
    Start([AddColumn]) --> GetName[columnName = column.Name]
    GetName --> CheckName{Is columnName in _columns dict?}
    
    CheckName -- Yes --> ThrowErr[Raise DuplicateColumnException]
    CheckName -- No --> Map[Store: _columns[columnName] = column]
    Map --> Finish([Return success])
```

## 2. `InsertRow(row)` Flowchart

```mermaid
flowchart TD
    Start([InsertRow]) --> ValidateLen{len(row.Values) == len(_columns)?}
    
    ValidateLen -- No --> ThrowErr[Raise ColumnMismatchException]
    ValidateLen -- Yes --> ValidateTypes{Are all value types valid for their columns?}
    
    ValidateTypes -- No --> ThrowErr2[Raise InvalidDataTypeException]
    ValidateTypes -- Yes --> AppendRow[Append row to _rows list]
    AppendRow --> Finish([Return success])
```
