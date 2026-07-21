# Database Objects: Test Cases & Contracts

This document outlines the test cases and class contracts for the top-level logical layer (Schema, Table, Column, Row, etc.).

## 1. Unit Test Cases (Flowchart)

```mermaid
flowchart LR
    Subsystem[Database Objects] --> Schema
    Schema --> AddTable_WhenTableIsValid_ShouldRegisterTable
    Schema --> AddTable_WhenNameAlreadyExists_ShouldThrow
    Schema --> RemoveTable_WhenTableExists_ShouldRemoveTable
    
    Subsystem --> Table
    Table --> InsertRow_WhenRowIsValid_ShouldInsertRow
    Table --> InsertRow_WhenSchemaDoesNotMatch_ShouldThrow
    Table --> AddColumn_WhenNameAlreadyExists_ShouldThrow
    
    Subsystem --> Column
    Column --> Create_WhenDefinitionIsValid_ShouldCreateColumn
    Column --> Create_WhenNameIsInvalid_ShouldThrow
    Column --> ValidateValue_WhenTypeDoesNotMatch_ShouldReturnFalse
    
    Subsystem --> Row
    Row --> GetValue_WhenColumnExists_ShouldReturnValue
    Row --> SetValue_WhenValueIsValid_ShouldUpdateValue
    Row --> SetValue_WhenTypeDoesNotMatch_ShouldThrow
    
    Subsystem --> Constraint
    Constraint --> Validate_WhenValueSatisfiesConstraint_ShouldSucceed
    Constraint --> Validate_WhenValueViolatesConstraint_ShouldFail
    Constraint --> Apply_WhenConstraintIsDisabled_ShouldSkipValidation
    
    Subsystem --> ForeignKey
    ForeignKey --> Validate_WhenParentRecordExists_ShouldSucceed
    ForeignKey --> Validate_WhenParentRecordDoesNotExist_ShouldFail
    ForeignKey --> DeleteParent_WhenRestricted_ShouldRejectDeletion
    
    Subsystem --> Index
    Index --> Insert_WhenKeyIsValid_ShouldAddEntry
    Index --> Search_WhenKeyExists_ShouldReturnRecordPointer
    Index --> Insert_WhenUniqueKeyAlreadyExists_ShouldThrow
    
    Subsystem --> Partition
    Partition --> RouteRow_WhenKeyMatchesRange_ShouldReturnPartition
    Partition --> RouteRow_WhenKeyIsOutsideRange_ShouldFail
    Partition --> AddRange_WhenRangesOverlap_ShouldThrow
    
    Subsystem --> View
    View --> Create_WhenQueryIsValid_ShouldCreateView
    View --> Resolve_WhenDependenciesExist_ShouldReturnDefinition
    View --> Resolve_WhenDependencyIsMissing_ShouldThrow
    
    Subsystem --> StoredProcedure
    StoredProcedure --> Execute_WhenParametersAreValid_ShouldReturnResult
    StoredProcedure --> Execute_WhenRequiredParameterIsMissing_ShouldThrow
    StoredProcedure --> Execute_WhenTransactionFails_ShouldPropagateFailure
```

## 2. Derived Method Contracts (Detailed Class Diagram)

Based on the test scenarios, the detailed components are structured as follows:

```mermaid
classDiagram
    direction TB

    class Schema {
        +string Name
        +AddTable(Table table) void
        +RemoveTable(string tableName) void
        +GetTable(string tableName) Table
        +ContainsTable(string tableName) bool
        +ResolveObject(string objectName) object
        +ContainsObject(string objectName) bool
    }

    class Table {
        +string Name
        +AddColumn(Column column) void
        +InsertRow(Row row) void
        +GetColumn(string columnName) Column
        +GetColumnIndex(Column column) int
        +ContainsColumn(string columnName) bool
        +ContainsRow(Row row) bool
        +GetPrimaryIndex() Index
        +GetForeignKeyIndex() Index
    }

    class Column {
        +string Name
        +string Type
        +Create(string name, string type) Column
        +ValidateValue(object value) bool
    }

    class Row {
        +object[] Values
        +GetValue(string columnName) object
        +SetValue(string columnName, object value) void
    }

    class Constraint {
        +bool IsEnabled
        +Check(object value) bool
        +Validate(object value) bool
        +Apply(object value) void
    }

    class ForeignKey {
        +string RefTable
        +DeleteBehavior DeleteBehavior
        +Validate(object parentKey) bool
        +ValidateParentDeletion(object parentKey) void
    }

    class Index {
        +bool IsUnique
        +Insert(object key, RecordPointer pointer) void
        +Search(object key) RecordPointer
    }

    class Partition {
        +string Range
        +RouteRow(Row row, string partitionKey) Partition
        +AddRange(string range) void
        +Contains(object key) bool
    }

    class View {
        +string Name
        +string Query
        +Create(string name, string query, Schema schema) View
        +Resolve(Schema schema) ViewDefinition
    }

    class StoredProcedure {
        +Execute(ParameterCollection parameters) object
        +ValidateParameters(ParameterCollection parameters) bool
    }

    class TransactionManager {
        +BeginTransaction() Transaction
        +Commit(Transaction transaction) void
        +Rollback(Transaction transaction) void
    }

    class ProcedureBody {
        +Execute(ParameterCollection parameters, Transaction transaction) object
    }

    Schema *-- Table
    Schema *-- View
    Schema *-- StoredProcedure

    Table *-- Column
    Table *-- Row
    Table *-- Constraint
    Table *-- Index
    Table *-- Partition

    Constraint <|-- ForeignKey

    StoredProcedure --> TransactionManager
    StoredProcedure --> ProcedureBody
```
