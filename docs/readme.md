# Design Patterns & Unit Testing Roadmap

This document outlines the core Design Patterns derived from the Feature Mindmap, Class Mindmap, and Test Cases. It defines the rationale for applying these patterns and how they integrate into the Test-Driven Development (TDD) lifecycle.

---

## TABLE 1: DATABASE OBJECTS (Logical Schema Layer)

| Feature / Class | Design Pattern | Problem & Rationale | Unit Test (TDD) Implementation Strategy |
| :--- | :--- | :--- | :--- |
| **Catalog Management**<br>`CatalogManager` | **Singleton** | The database instance must have one centralized, globally accessible registry for all schemas to prevent synchronization conflicts. | Test accessing the instance from multiple parallel threads to ensure only one memory address is generated. |
| **Table Creation**<br>`SchemaBuilder`, `TableBuilder` | **Nested Builder** | Initializing a hierarchy (Schema contains Tables, Tables contain Columns) is bulky. Nested Builders allow cascading fluent configurations. | Test the fluent method chaining (`.with_table().with_column().build()`) to verify it returns a valid composite tree without missing nodes. |
| **Constraint Validation**<br>`Constraint` (Base) | **Strategy** | Extracts validation logic (Check, Unique) away from the `Table` class, preventing the `insert_row` method from bloating with if/else chains. | Test using isolated mock strategies or simulated bad data rows to catch specific `ConstraintViolationException` violations. |
| **Validation Context**<br>`ConstraintContext` | **Parameter Object** | Reduces method signature bloat (avoid passing `row`, `table`, `schema` individually). Packages all validation state into a single immutable context envelope. | Test that the context successfully binds references to the input Table and Row without mutating them. |
| **Referential Integrity**<br>`ForeignKeyConstraint`,<br>`IReferentialAction` | **Strategy** | Hardcoding `CASCADE` vs `RESTRICT` logic inside the Table creates spaghetti code. Exposing them as interchangeable strategies allows dynamic FK behavior. | Create mock actions (`CascadeAction`, `RestrictAction`) and test if the parent deletion successfully triggers the correct child table cascade or exception. |
| **Index Creation**<br>`IndexFactory` | **Factory Method** | The DBMS supports various Index types (Hash, B-Tree). The core system shouldn't hardcode their instantiation. | Call the Factory with a flag (`type="BTREE"`) and test if the inserted Node correctly routes through the B-Tree logic flow. |
| **Column Definition**<br>`Column`, `ColumnBuilder` | **Value Object** | A Column is immutable after creation (name + type fixed). Enforces that structure cannot mutate during runtime. | Test that two Columns with same name/type are equal, and that mutating properties raises an error. |
| **Row Data**<br>`Row` | **Value Object** | A Row represents a snapshot of data at insert time. Immutable values prevent dirty reads and concurrent modification bugs. | Test that Row is constructed with fixed-length values matching Column schema, and equality is value-based not reference-based. |
| **Database Entry Point**<br>`Database` | **Facade** | `Database` wraps the `CatalogManager` + `SchemaBuilder` internals and exposes a clean API: `create_schema`, `drop_schema`, `get_schema`. The caller never touches the subsystems directly. | Test that calling `db.create_schema("public")` correctly persists the schema through `CatalogManager`. |
| **Database Lifecycle**<br>`DatabaseCatalog` | **Factory Method** | Controls the creation and deletion of `Database` objects. Prevents duplicate names and acts as the single source of truth for all active databases, mirroring `IndexFactory`. | Test that `DatabaseCatalog.create_database("Tiki")` returns a `Database` instance, and that creating a duplicate name raises `DatabaseExistsException`. |
| **Data Partitioning**<br>`PartitionStrategy` | **Strategy Pattern** | Routing rows across multiple partition ranges shouldn't clutter the main `Table`'s `insert_row` logic. Delegating the routing handles Overlaps, Boundaries, and Not-Found cleanly. | Test `route_row` on explicit mathematical boundaries. Test that overlapping ranges throw `PartitionRangeOverlapException`. |
| **Schema Management**<br>`Schema`, `DatabaseObject` | **Composite Pattern** | Managing Tables, Views, and Sequences as explicit disparate types makes Schema code messy. Using a Component interface (`DatabaseObject`) allows treating all Leaf objects uniformly. | Test that `Table`, `View`, and `Sequence` can all be added generically to the Schema, and that calling `drop()` cascades correctly. |
| **Virtual Tables**<br>`View` | **Proxy / Adapter Pattern** | A View acts as a virtual table, shielding users from complex joins. It proxies `SELECT` queries to underlying tables without physically storing data. | Test that `resolve(schema)` correctly throws `NotImplementedError` or translates the query using actual Schema objects safely. |
| **Auto Increment ID**<br>`Sequence` | **State Pattern** | Sequences must maintain a thread-safe incrementing state across concurrent inserts across the DBMS system. | Test that traversing `next_value()` incrementally increments the state, and limits are respected. |
| **Executable Logic**<br>`StoredProcedure` | **Command Pattern** | Allows defining and packaging custom procedural SQL/Logic into isolated, executable blocks. The system simply blind-triggers `execute()`. | Test that invoking `execute()` with parameters successfully delegates to the underlying runtime environment. |


### 1.1. Sequence Diagram: Builder Pattern
```mermaid
sequenceDiagram
    participant Client
    participant S_Build as SchemaBuilder
    participant T_Build as TableBuilder
    participant Schema
    participant Table
    
    Client->>S_Build: new SchemaBuilder("public")
    activate S_Build
    
    Client->>S_Build: with_table("users")
    S_Build->>T_Build: create("users")
    activate T_Build
    T_Build->>T_Build: with_column("id")
    T_Build->>T_Build: with_column("name")
    T_Build-->>S_Build: return TableBuilder
    deactivate T_Build
    
    Client->>S_Build: build()
    S_Build->>Schema: instantiate()
    S_Build->>T_Build: build()
    T_Build->>Table: instantiate()
    T_Build-->>Schema: add_table(Table)
    S_Build-->>Client: return Schema
    deactivate S_Build
```

### 1.2. Sequence Diagram: Strategy Pattern (Constraint)
```mermaid
sequenceDiagram
    participant Test as Unit Test
    participant Table
    participant Val as IConstraintValidator (Unique)
    
    Test->>Table: add_validator(Val)
    Test->>Table: insert_row(row)
    activate Table
    Table->>Val: validate(row)
    alt Value matches
        Val-->>Table: true
        Table->>Table: _rows.append(row)
        Table-->>Test: void
    else Duplicate Value
        Val-->>Table: throw ConstraintViolationException
        Table-->>Test: throw Exception (Caught by Test)
    end
    deactivate Table
```

### 1.3. Sequence Diagram: Singleton Pattern (CatalogManager)
```mermaid
sequenceDiagram
    participant Test as Unit Test
    participant CM as CatalogManager
    participant RAM as Memory (_instance)
    
    Test->>CM: new CatalogManager()
    activate CM
    CM->>CM: py__new__()
    alt _instance is None (First Call)
        CM->>RAM: Allocate Memory
        CM->>CM: Create _schemas{} Dictionary
    end
    CM-->>Test: return RAM Address
    deactivate CM
    
    Test->>CM: new CatalogManager() (Second Call)
    activate CM
    CM->>CM: py__new__()
    alt _instance already exists
        CM-->>Test: return same RAM Address
    end
    deactivate CM
```

### 1.4. Sequence Diagram: Factory Method (IndexFactory)
```mermaid
sequenceDiagram
    participant Client as Unit Test
    participant Factory as IndexFactory
    participant BTree as BTreeIndex
    participant Hash as HashIndex
    
    Client->>Factory: create_index("BTREE", "idx_id", ["id"])
    activate Factory
    alt type == "BTREE"
        Factory->>BTree: instantiate
        BTree-->>Factory: BTreeIndex object
    else type == "HASH"
        Factory->>Hash: instantiate
        Hash-->>Factory: HashIndex object
    else invalid type
        Factory-->>Client: throw ValueError
    end
    Factory-->>Client: return Index object
    deactivate Factory
```

### 1.5. Sequence Diagram: Table-Index Integration (insert_row flow)
```mermaid
sequenceDiagram
    participant Client
    participant Table
    participant Val as IConstraintValidator (Strategy)
    participant Factory as IndexFactory
    participant Idx as Index (BTree/Hash)

    Client->>Table: insert_row(row)
    activate Table

    Table->>Table: _validate_value_count(row)
    alt Column count mismatch
        Table-->>Client: throw RowSchemaMismatchException
    end

    loop Each validator in _validators
        Table->>Val: validate(ConstraintContext)
        alt Violation detected
            Val-->>Table: throw ConstraintViolationException
            Table-->>Client: propagate exception
        else OK
            Val-->>Table: true
        end
    end

    Table->>Table: _rows.append(row)

    loop Each index in _indexes
        Table->>Idx: insert(key, record_pointer)
        Idx-->>Table: void
    end

    Table-->>Client: void
    deactivate Table
```

### 1.6. Sequence Diagram: Factory Method & Facade (Database Lifecycle)
```mermaid
sequenceDiagram
    participant Client
    participant DC as DatabaseCatalog (Factory)
    participant DB as Database (Facade)
    participant CM as CatalogManager (Singleton)

    %% Phase 1: Factory Creates Database
    Client->>DC: create_database("ecommerce")
    activate DC
    DC->>DC: Check name collision
    DC->>DB: new Database("ecommerce")
    DB-->>DC: Database instance
    DC-->>Client: return Database object
    deactivate DC

    %% Phase 2: Facade Delegates Schema Creation
    Client->>DB: create_schema("public")
    activate DB
    DB->>CM: add_schema(schema object)
    CM-->>DB: success
    DB-->>Client: void
    deactivate DB
```

### 1.6. Sequence Diagram: Value Object (Row / Column Immutability)
```mermaid
sequenceDiagram
    participant Client
    participant VO as Row / Column (Value Object)
    participant RAM as Internal State (Tuple)

    %% Flow 1: Creation and Type Enforcement 
    Client->>VO: new Row([1, "Alice"])
    activate VO
    VO->>RAM: Encapsulate as read-only Tuple
    VO-->>Client: instance
    deactivate VO
    
    %% Flow 2: Attempting Dirty Write Mutation
    Client-xVO: row._values[0] = 5
    activate VO
    VO-->>Client: Throw TypeError / AttributeError
    deactivate VO
    
    %% Flow 3: Value Equality Comparison
    Client->>VO: __eq__(other_row)
    activate VO
    VO->>RAM: Self.Tuple == Other.Tuple
    RAM-->>VO: compare data purely
    VO-->>Client: return boolean
    deactivate VO
```

---

## TABLE 2: STORAGE & TRANSACTION ENGINE (Physical Hardware Layer)

| Feature / Class | Design Pattern | Problem & Rationale | Unit Test (TDD) Implementation Strategy |
| :--- | :--- | :--- | :--- |
| **Memory / Cache Management**<br>`BufferPoolManager` | **Proxy / Object Pool** | Direct Disk I/O is slow. Serves as a gateway to recycle RAM memory and minimize disk hits. | Generate mock Page Requests, testing the LRU Eviction behavior when the RAM buffer pool reaches full capacity. |
| **ACID Recovery**<br>`LogCommand`, `WAL` | **Command / Observer** | Wraps Undo/Redo operations as executable Commands. Triggers the Write-Ahead Log (WAL) to flush to disk upon Commit. | Create a pseudo-array of Commands (Insert, Update), simulate a system crash, and verify the WAL file reconstructs the uncommitted states. |

### 2.1. Sequence Diagram: Buffer Pool (Proxy Pattern)
```mermaid
sequenceDiagram
    participant Test as Unit Test
    participant Pool as BufferPoolManager
    participant Disk as FileManager
    
    Test->>Pool: fetch_page(id=5)
    activate Pool
    Pool->>Pool: is in Cache (RAM)?
    alt Yes
        Pool-->>Test: return Page(5)
    else No (Cache Miss)
        Pool->>Disk: read_block(5)
        Disk-->>Pool: data
        Pool->>Pool: LRU.evict() if full
        Pool-->>Test: return Page(5)
    end
    deactivate Pool
```

---

## TABLE 3: QUERY PROCESSING (Execution & Translation Engine)

| Feature / Class | Design Pattern | Problem & Rationale | Unit Test (TDD) Implementation Strategy |
| :--- | :--- | :--- | :--- |
| **SQL Parser**<br>`SqlVisitor`, `ASTNode` | **Visitor** | The Abstract Syntax Tree (AST) structure is highly nested. A Visitor transverses the nodes cleanly to extract meaning. | Supply a simulated AST tree hierarchy (Root -> Node -> Leaf) and verify the Visitor correctly reads and translates specific Node tokens. |
| **Execution Framework**<br>`AbstractPlanNode` | **Template Method** | Base plan nodes share common startup/teardown logic but execute differently. | Test abstract inheritance ensuring `open()` is always called before child-specific `execute()`. |
| **Query Engine**<br>`AbstractPlanNode` | **Iterator (Volcano Model)** | Prevents loading massive tables entirely into RAM. Provides a `Next()` method to yield results row-by-row sequentially. | Chain a `ScanNode` to a `FilterNode`, and perform continuous `next()` calls to verify records are dropped until reaching an EOF/Null. |

### 3.1. Sequence Diagram: Iterator Pattern (Volcano Execution)
```mermaid
sequenceDiagram
    participant Test as Unit Test
    participant Filter as FilterNode
    participant Scan as ScanNode
    
    Test->>Filter: open()
    Filter->>Scan: open()
    
    Test->>Filter: next()
    activate Filter
    Filter->>Scan: next()
    Scan-->>Filter: return raw_row
    Filter->>Filter: check predicate
    Filter-->>Test: return valid_row
    deactivate Filter
```
