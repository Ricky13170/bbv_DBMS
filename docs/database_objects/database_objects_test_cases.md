# Database Objects: Test Cases & Contracts

This document outlines the test cases and class contracts for the top-level logical layer (Schema, Table, Column, Row, etc.).

## 1. Unit Test Cases (Flowchart)

```mermaid
flowchart LR
    Subsystem[Database Objects Tests]
    
    %% Core Management Tests
    Subsystem --> CM[CatalogManager Singleton]
    CM --> CM_Singleton[AddSchema_WhenInstanceRequested_ReturnsSameSingleton]
    CM --> CM_State[GetSchema_WhenSchemaMissing_ShouldThrowError]
    
    Subsystem --> DC[DatabaseCatalog Factory]
    DC --> DC_Create[CreateDatabase_WhenNameIsValid_ReturnsDatabaseFacade]
    DC --> DC_Conflict[CreateDatabase_WhenNameExists_ThrowsException]
    
    Subsystem --> Facade[Database Facade]
    Facade --> DB_CreateSchema[CreateSchema_DelegatesToCatalogManager]
    
    %% Builder Tests
    Subsystem --> Builders[Schema & Table Builders]
    Builders --> BuildSchema[SchemaBuilder_WithTable_BuildsCompositeSchema]
    Builders --> BuildTable[TableBuilder_WithColumn_BuildsLeafTable]
    
    %% Composite Tests
    Subsystem --> Composite[Schema & Table Composite]
    Composite --> Schema_AddTable[AddTable_WhenValid_RegistersTable]
    Composite --> Table_InsertRow[InsertRow_WhenValidRow_AddsToTable]
    Composite --> DDL_Drop[Drop_WhenInvoked_ExecutesCleanup]
    
    %% Value Object Tests
    Subsystem --> VO[Column & Row Value Objects]
    VO --> Col_InvalidType[Init_WhenTypeUnsupported_ThrowsValueError]
    VO --> Row_Immutability[Init_WhenCreated_TuplePreventsMutation]
    
    %% Strategy Tests
    Subsystem --> Strategy[Constraint & Partition Strategy]
    Strategy --> Ctx_Strategy[Validate_WithConstraintContext_ReturnsBoolean]
    Strategy --> FK_Strategy[Validate_DelegatesToReferentialActionStrategy]
    Strategy --> Routing[RouteRow_WhenKeyMatches_DelegatesToPartition]
    
    %% Behavior Pattern Tests
    Subsystem --> Behaviors[View, Sequence, StoredProcedure]
    Behaviors --> View_Proxy[Resolve_WhenCalled_ActsAsVirtualProxy]
    Behaviors --> Seq_State[NextValue_WhenCalled_UpdatesInternalState]
    Behaviors --> Proc_Command[Execute_WhenInvoked_ExecutesCommandLogic]
    
    %% Factory Tests
    Subsystem --> Factory[IndexFactory]
    Factory --> Idx_Create[Create_WhenTypeIsBTree_ReturnsBTreeIndex]
    Factory --> Idx_Unsupported[Create_WhenTypeUnsupported_ThrowsValueError]
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
