# Advanced Patterns: Database Objects (Core 20%)

This document formalizes the **Top-Down Design** of the advanced 20% core features using robust OOP and SOLID principles.

## 1. TableBuilder (Builder Pattern)

**Problem:** Initializing a `Table` with columns, metadata, and constraints via a massive constructor or procedural `add_xxx` methods violates the Open/Closed Principle and makes client code messy.  
**Solution (OOP):** Implement a Fluent `TableBuilder` that incrementally configures the table and verifies its sanity before returning the final immutable `Table` object.

### A. Detailed Class Diagram

```mermaid
classDiagram
    direction LR
    
    class Table {
        +string Name
        -Dict _columns
        -List _constraints
        +InsertRow(Row row)
    }

    class TableBuilder {
        -Table _table
        +TableBuilder(string tableName)
        +WithStringColumn(string name, int length) TableBuilder
        +WithIntColumn(string name) TableBuilder
        +WithPrimaryKey(string columnName) TableBuilder
        +WithNotNullConstraint(string columnName) TableBuilder
        +Build() Table
    }

    TableBuilder ..> Table : Creates & Configures
```

### B. Sequence Diagram (Client Usage)

```mermaid
sequenceDiagram
    participant Client
    participant Builder as TableBuilder
    
    Client->>Builder: new TableBuilder("users")
    activate Builder
    
    Client->>Builder: WithIntColumn("id")
    Builder->>Builder: _table.add_column(...)
    Builder-->>Client: return self
    
    Client->>Builder: WithStringColumn("name", 50)
    Builder->>Builder: _table.add_column(...)
    Builder-->>Client: return self
    
    Client->>Builder: Build()
    Builder->>Builder: Check Table Sanity (at least 1 col)
    
    alt Table is Invalid
        Builder-->>Client: Raise InvalidTableDefinitionException
    else Table is Valid
        Builder-->>Client: return Table object
    end
    deactivate Builder
```

---

## 2. Constraint Validation (Strategy Pattern)

**Problem:** Putting `if constraint == "NOT_NULL": ... elif constraint == "UNIQUE": ...` inside `Table.InsertRow` violates the Single Responsibility Principle (SRP) and Open/Closed Principle (OCP).  
**Solution (SOLID):** Extract the validation algorithm into an `IConstraintValidator` interface. The `Table` loops through a list of injected strategies.

### A. Detailed Class Diagram

```mermaid
classDiagram
    direction TB
    
    class Table {
        -List~IConstraintValidator~ _validators
        +AddValidator(IConstraintValidator v)
        +InsertRow(Row row)
    }

    class IConstraintValidator {
        <<interface>>
        +Validate(Row row, Table table) bool
    }

    class NotNullValidator {
        -string _columnName
        +Validate(...) bool
    }

    class UniqueValidator {
        -string _columnName
        +Validate(...) bool
    }

    class CheckRegexValidator {
        -string _columnName
        -string _pattern
        +Validate(...) bool
    }

    Table "1" *-- "many" IConstraintValidator : uses
    IConstraintValidator <|.. NotNullValidator
    IConstraintValidator <|.. UniqueValidator
    IConstraintValidator <|.. CheckRegexValidator
```

### B. `InsertRow` Internal Flowchart (Applying Strategies)

```mermaid
flowchart TD
    Start([InsertRow(row)]) --> PreCheck{Row match Columns length?}
    
    PreCheck -- No --> Throw1[Raise ColumnMismatchException]
    PreCheck -- Yes --> Loop[Loop through _validators list]
    
    Loop --> HasNext{Has next validator?}
    
    HasNext -- Yes --> ValCheck[validator.Validate(row, self)]
    ValCheck --> CheckResult{Is Valid?}
    
    CheckResult -- No --> Throw2[Raise ConstraintViolationException]
    CheckResult -- Yes --> Loop
    
    HasNext -- No --> Append[self._rows.append(row)]
    Append --> End([Return Success])
```
