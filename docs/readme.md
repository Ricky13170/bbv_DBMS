# Design Patterns & Unit Testing Roadmap

This document outlines the core Design Patterns derived from the Feature Mindmap, Class Mindmap, and Test Cases. It defines the rationale for applying these patterns and how they integrate into the Test-Driven Development (TDD) lifecycle.

---

## TABLE 1: DATABASE OBJECTS (Logical Schema Layer)

| Priority | Feature / Class | Design Pattern | Problem & Architecture Need | Application / Usage | Unit Test (TDD) Implementation Strategy |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **P1** | `CatalogManager` | **Singleton** | A DBMS must have exactly one global registry for all schemas. Multiple instances would lead to split-brain state synchronization bugs. | `cm1 = CatalogManager()`<br>`cm2 = CatalogManager()`<br>`assert cm1 is cm2 # True` | Test that concurrent thread access always returns the same memory address. Verify that `add_schema()` persists across calls. |
| **P1** | `DatabaseCatalog` | **Factory Method** | Centralizes `Database` object creation. Prevents duplicate DB names and keeps the system as the single source of truth for all active databases. | `db = DatabaseCatalog.create_database("Tiki")`<br>`# Duplicate → raise DatabaseExistsException` | Test that `create_database("X")` returns a `Database`, and that calling it again with `"X"` raises `DatabaseExistsException`. |
| **P1** | `Database` | **Facade** | The `Database` class must shield the client from internal complexity (CatalogManager + SchemaBuilder). Client only needs one clean API. | `db.create_schema("public")`<br>`# Client never sees CatalogManager internally` | Test that `create_schema("public")` persists the schema, and `get_schema()` returns the same object. |
| **P1** | `Schema`, `DatabaseObject` | **Composite Pattern** | A Schema contains Tables, Views, Sequences. Drop operations must propagate uniformly without type-checking each child. | `schema.drop()`<br>`# Internally calls .drop() on ALL children,`<br>`# regardless of whether they are Table or View` | Test that `add_table()`, `add_view()`, and `add_sequence()` are accepted uniformly. Test `drop()` cascades without errors. |
| **P1** | `SchemaBuilder` | **Builder Pattern** | Constructing a full Schema requires complex Setup. Fluent Builder abstraction removes structural noise. | `schema = SchemaBuilder("db")`<br>`.with_table("users").build()` | Test fluent chaining builds a valid Schema tree. Test missing fields raise `ValueError`. |
| **P1** | `TableBuilder` | **Builder Pattern** | Initializing a Table with dozens of Columns/Constraints manually causes bloated constructors. | `table = TableBuilder("users")`<br>`.with_column("id", "int").build()` | Test fluent column accumulation. Test duplicate columns raise Exceptions. |
| **P1** | `Column` | **Value Object** | Once a column is defined (name + type), it must not mutate. Immutability prevents inconsistent schema drift at runtime. | `col = Column("id", "int")`<br>`col.name = "x" # Raises AttributeError`<br>`Column("id","int") == Column("id","int") # True` | Test that post-creation mutation raises `AttributeError`. Test that two columns with equal fields are equal via `__eq__`. |
| **P1** | `Row` | **Value Object** | A Row is a snapshot of data at insert-time. Mutable rows cause dirty reads in concurrent environments. | `r1 = Row((1, "Alice"))`<br>`r1.values[0] = 99 # Raises TypeError`<br>`Row((1,"A")) == Row((1,"A")) # True` | Test that all values are wrapped in an immutable tuple. Test equality is value-based, not reference-based. |
| **P1** | `Constraint` | **Strategy Pattern** | Validation logic (Check, Unique, Not Null) embedded inside `Table.insert_row` creates unreadable bloat. Strategy externalizes each rule as a swappable object. | `unique_validator.validate(ctx)`<br>`# Table loops validators without knowing their type` | Test each strategy independently with mock contexts. Test `ConstraintViolationException` for a bad row, and `True` for a valid one. |
| **P1** | `ConstraintContext` | **Parameter Object** | Passing `row, table, schema` as separate arguments to every validator bloats method signatures. One immutable envelope bundles all state. | `ctx = ConstraintContext(row, table)`<br>`validator.validate(ctx) # Single clean argument` | Test that the context binds references to Table and Row without mutating their internal state. |
| **P2** | `ForeignKeyConstraint`, `IReferentialAction` | **Strategy Pattern** | Hardcoding `CASCADE` or `RESTRICT` inside Table classes creates spaghetti. Injecting strategies allows dynamic FK behavior at creation time. | `fk = ForeignKeyConstraint("user_id",`<br>`    on_delete=CascadeAction())`<br>`# Deleting parent → auto cascade to child` | Create mock `CascadeAction` and `RestrictAction`. Test parent deletion correctly triggers child cascade or exception. |
| **P2** | `IndexFactory` | **Factory Method** | DBMS supports different Index types (B-Tree, Hash). Core classes must not hardcode algorithm instantiation. | `idx = IndexFactory.create("BTREE")`<br>`idx.insert("alice", ptr) # Type-specific impl.` | Test `create("BTREE")` returns a B-Tree instance and `create("HASH")` a Hash instance. Test invalid types raise `ValueError`. |
| **P2** | `PartitionStrategy` | **Strategy Pattern** | Row routing to physical partitions (by key range) must not clutter the main `Table.insert_row` logic with boundary conditions. | `partition_name = strategy.route_row(row.key)`<br>`# Table blindly delegates routing to Strategy` | Test exact boundary conditions (in-range returns partition name). Test out-of-range throws `PartitionNotFoundException`. Overlapping ranges throw `PartitionRangeOverlapException`. |
| **P3** | `Sequence` | **State Pattern** | Auto-numbering (e.g. `AUTO_INCREMENT`) must maintain a thread-safe, in-memory counter that advances precisely. | `seq = Sequence("id_seq", start=1, increment=1)`<br>`seq.next_value() # → 1`<br>`seq.next_value() # → 2` | Test that `next_value()` advances by exactly `increment`. Test multiple calls return strictly sequential values with no skips. |
| **P3** | `View` | **Proxy / Adapter** | A View hides multi-table JOINs behind a virtual table interface. Client queries `my_view` as if it were a real Table, unaware of the complexity. | `view = View("active_users", "SELECT * FROM users WHERE active=1")`<br>`result = view.resolve(schema) # Proxies query to Engine` | Test `resolve(schema)` returns compiled output. Test that a missing dependency table raises `DependencyViolationException`. |
| **P3** | `StoredProcedure` | **Command Pattern** | Pre-packaged SQL logic must be callable without the client knowing the internals. The system only needs to trigger `execute()`. | `proc = StoredProcedure("clean_logs", body="DELETE...")`<br>`proc.execute(days=30) # Triggers encapsulated logic` | Test `execute(params)` delegates correctly. Test a missing required parameter raises `TypeError`. Test transaction failures propagate upward. |



### 1.1. Sequence Diagram: Singleton Pattern (CatalogManager)
```mermaid
sequenceDiagram
    participant Client
    participant CM as CatalogManager
    participant RAM as Memory (_instance)
    
    Client->>CM: new CatalogManager()
    activate CM
    CM->>CM: py__new__()
    
    alt _instance is None
        CM->>RAM: Allocate Memory
        CM->>CM: Create _schemas{} Dictionary
        CM-->>Client: return New RAM Address
    else _instance already exists
        CM-->>Client: return same RAM Address
    end
    deactivate CM
```


### 1.2. Sequence Diagram: Factory Method (DatabaseCatalog)
```mermaid
sequenceDiagram
    participant Client
    participant DC as DatabaseCatalog (Factory)
    participant DB as Database (Facade)

    Client->>DC: create_database("ecommerce")
    activate DC
    DC->>DC: Check for Name collision
    alt Name Already Exists
        DC-->>Client: throw DatabaseExistsException
    else Valid Name
        DC->>DB: new Database("ecommerce")
        DB-->>DC: Database instance
        DC->>DC: Register db into _databases{}
        DC-->>Client: return Database object
    end
    deactivate DC
```

### 1.3. Sequence Diagram: Facade Pattern (Database API)
```mermaid
sequenceDiagram
    participant Client
    participant DB as Database (Facade)
    participant CM as CatalogManager (Singleton)
    participant SB as SchemaBuilder

    Client->>DB: create_schema("public")
    activate DB
    DB->>SB: Instantiate SchemaBuilder("public").build()
    SB-->>DB: Return clean Schema tree
    DB->>CM: Pass to CatalogManager for storage
    CM-->>DB: Flag persist success
    DB-->>Client: void (Client is completely blind to CM or SB)
    deactivate DB
```

### 1.4. Sequence Diagram: Composite Pattern (Schema Drop)
```mermaid
sequenceDiagram
    participant Client
    participant Sch as Schema (Composite)
    participant Tbl as Table (Leaf)
    participant View as View (Leaf)

    Client->>Sch: drop()
    activate Sch
    Sch->>Sch: Iterate over self._objects list
    
    loop For each DatabaseObject
        alt object is Table
            Sch->>Tbl: drop()
            Tbl-->>Sch: void
        else object is View
            Sch->>View: drop()
            View-->>Sch: void
        end
    end
    Sch-->>Client: void
    deactivate Sch
```

### 1.5. Sequence Diagram: Builder Pattern (Table Creation)
```mermaid
sequenceDiagram
    participant Client
    participant TB as TableBuilder
    participant Col as Column
    participant Tbl as Table
    
    Client->>TB: new TableBuilder("users")
    activate TB
    
    Client->>TB: with_column("id", "int")
    TB->>Col: new Column("id", "int")
    Col-->>TB: Column instance
    TB->>TB: Lưu Column vào self._columns[]
    
    Client->>TB: build()
    TB->>Tbl: new Table("users")
    TB->>Tbl: Đổ danh sách _columns vào Table
    Tbl-->>TB: Table instance sạch sẽ
    TB-->>Client: return Table
    deactivate TB
```

### 1.6. Sequence Diagram: Builder Pattern (SchemaBuilder)
```mermaid
sequenceDiagram
    participant Client
    participant SB as SchemaBuilder
    participant TB as TableBuilder
    participant Sch as Schema
    
    Client->>SB: new SchemaBuilder("public")
    activate SB
    
    Client->>SB: with_table("users")
    SB->>TB: new TableBuilder("users")
    activate TB
    TB-->>SB: TableBuilder Reference
    SB->>SB: Lưu TB vào self._table_builders[]
    
    %% Triggers Fluent Chaining directly on the returned TB
    Client->>TB: with_column("id", "int")
    
    Client->>SB: build()
    SB->>Sch: new Schema("public")
    
    loop Dọn dẹp nhà thầu phụ
        SB->>TB: build()
        TB-->>SB: Table instance
        SB->>Sch: add_table(Table)
    end
    
    Sch-->>SB: Schema instance hoàn mỹ
    SB-->>Client: return Schema
    deactivate TB
    deactivate SB
```

### 1.7. Sequence Diagram: Value Object (Row / Column Immutability)
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
### 1.8. Sequence Diagram: Strategy Pattern (Constraint)
```mermaid
sequenceDiagram
    participant Test as Unit Test
    participant Table
    participant Val as Constraint (Strategy)
    participant Ctx as ConstraintContext (Parameter Object)
    
    Test->>Table: add_constraint(Val)
    Test->>Table: insert_row(row)
    activate Table
    
    %% Tạo giỏ Parameter chứa cả row mồi, table hiện tại và schema tổng
    Table->>Ctx: new ConstraintContext(row, table, schema)
    
    Table->>Val: validate(Ctx)
    alt Xuyên biên giới an toàn
        Val-->>Table: true
        Table->>Table: _rows.append(row)
        Table-->>Test: void
    else Bị tóm cổ (Vi phạm)
        Val-->>Table: throw ConstraintViolationException
        Table-->>Test: throw Exception (Test đón lõng)
    end
    deactivate Table
```

### 1.9. Sequence Diagram: Strategy Pattern (Referential Integrity)
```mermaid
sequenceDiagram
    participant Table
    participant FK as ForeignKeyConstraint
    participant Action as IReferentialAction (Strategy)
    participant ChildTable
    
    %% Khi một hàng cha bị xóa đi
    Table->>FK: notify_parent_deleted(parent_row)
    activate FK
    FK->>Action: execute(parent_row, child_table)
    activate Action
    
    %% Quyền sinh sát lúc này nằm trong tay Strategy
    alt Strategy là Cascade
        Action->>ChildTable: delete_rows(foreign_key = target)
        ChildTable-->>Action: void
    else Strategy là Restrict
        Action-->>FK: throw ConstraintViolationException
    else Strategy là SetNull
        Action->>ChildTable: update_rows(foreign_key = target, NULL)
        ChildTable-->>Action: void
    end
    
    Action-->>FK: báo cáo kết quả
    deactivate Action
    FK-->>Table: void / Exception propagation
    deactivate FK
```

### 1.10. Sequence Diagram: Factory Method (IndexFactory)
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
    Factory-->>Client: return Index object (BTree/Hash giấu mặt)
    deactivate Factory
```

### 1.11. Sequence Diagram: Strategy Pattern (PartitionStrategy)
```mermaid
sequenceDiagram
    participant Client
    participant Table
    participant PStrat as PartitionStrategy
    participant PartA as Table (Partition Q1)
    
    %% Setup (Admin cấu hình trước)
    Client->>PStrat: add_range("Q1", "2023-01", "2023-03")
    
    %% Insertion (Lúc đẩy data thật vào)
    Client->>Table: insert_row(row)
    activate Table
    Table->>PStrat: route_row(row.date)
    activate PStrat
    
    alt Thuộc dải Q1
        PStrat-->>Table: return "Q1"
        Table->>PartA: insert_row(row)
    else Thuộc dải dở dang / Không tìm thấy
        PStrat-->>Table: throw PartitionNotFoundException
        Table-->>Client: Nhè thẳng Exception ra bắt Client nhập lại
    end
    deactivate PStrat
    
    Table-->>Client: void
    deactivate Table
```

### 1.12. High-Level Class Diagram (Structural View)
```mermaid
classDiagram
    %% Core Singleton & Factories
    class CatalogManager {
        <<Singleton>>
        -schemas: dict
        +add_schema()
    }
    class DatabaseCatalog {
        <<Factory Method>>
        -databases: dict
        +create_database(name) Database
    }
    class Database {
        <<Facade>>
        +create_schema(name)
    }
    
    DatabaseCatalog --> Database: creates
    Database --> CatalogManager: delegates to

    %% Composite Pattern (Database Objects)
    class DatabaseObject {
        <<Abstract>>
        +name: str
        +create()
        +drop()
    }
    class Schema {
        <<Composite>>
        -_tables: List[Table]
        -_views: List[View]
        +add_table(t: Table)
    }
    class Table {
        <<Leaf>>
        +insert_row()
    }
    class View {
        <<Proxy>>
        +resolve()
    }
    class Sequence {
        <<State>>
        +next_value()
    }
    class StoredProcedure {
        <<Command>>
        +execute()
    }

    DatabaseObject <|-- Schema
    DatabaseObject <|-- Table
    DatabaseObject <|-- View
    DatabaseObject <|-- Sequence
    DatabaseObject <|-- StoredProcedure
    
    %% Semantic relationship: Schema encapsulates Leaf objects
    Schema o-- DatabaseObject : containing

    %% Table Internal Strategies & Value Objects
    class PartitionStrategy {
        <<Strategy>>
        +route_row(key)
    }
    class Constraint {
        <<Strategy Base>>
        +validate(ctx: ConstraintContext)
    }
    class Column {
        <<Value Object>>
        +validate_value()
    }
    class Row {
        <<Value Object>>
        +values: Tuple
    }
    class Index {
        <<Physical Mapping>>
        +insert()
    }
    
    Table *-- Column
    Table *-- Row
    Table *-- Constraint
    Table *-- Index
    Table --> PartitionStrategy : delegates routing
```

### 1.11. Detailed Class Diagram (API & Methods mapped from TDD)
```mermaid
classDiagram
    %% Core Singleton & Factories
    class DatabaseCatalog {
        +create_database(name: str) Database
        +get_database(name: str) Database
        +drop_database(name: str)
    }
    class CatalogManager {
        +add_schema(schema: Schema)
        +get_schema(name: str) Schema
    }
    class Database {
        +create_schema(name: str)
        +drop_schema(name: str)
        +get_schema(name: str) Schema
    }
    
    %% Composite Pattern (Database Objects)
    class DatabaseObject {
        <<Abstract>>
        +name: str
        +create()
        +drop()
    }
    class Schema {
        +owner: str
        +add_table(t: Table)
        +get_table(name: str) Table
        +drop_table(name: str)
        +add_view(v: View)
        +add_sequence(s: Sequence)
        +add_procedure(p: StoredProcedure)
    }
    class Table {
        +add_column(c: Column)
        +drop_column(name: str)
        +alter_column(name, c: Column)
        +add_constraint(c: Constraint)
        +drop_constraint(name: str)
        +add_index(idx: Index)
        +insert_row(row: Row)
        +update_row(old_row: Row, new_row: Row)
        +delete_row(row: Row)
    }
    class View {
        +query_definition: str
        +resolve(schema: Schema) str
    }
    class Sequence {
        +start: int
        +increment: int
        +next_value() int
    }
    class StoredProcedure {
        +body: str
        +execute(*args, **kwargs)
    }

    DatabaseObject <|-- Schema
    DatabaseObject <|-- Table
    DatabaseObject <|-- View
    DatabaseObject <|-- Sequence
    DatabaseObject <|-- StoredProcedure
    
    %% Semantic relationship: Schema encapsulates Leaf objects
    Schema o-- DatabaseObject : containing

    %% Table Internal Strategies & Value Objects
    class PartitionStrategy {
        +add_range(name, start, end)
        +remove_range(name: str)
        +route_row(key: Any) str
    }
    class Constraint {
        <<Abstract Strategy>>
        +validate(ctx: ConstraintContext)
    }
    class Column {
        +name: str
        +data_type: str
        +is_nullable: bool
        +is_primary: bool
        +validate_value(value: Any) bool
    }
    class Row {
        +values: Tuple
    }
    class Index {
        +is_unique: bool
        +allows_null: bool
        +insert(key: Any, ptr: Any)
        +search(key: Any) List
        +delete(key: Any, ptr: Any)
        +range_search(start, end) List
    }
    
    Table *-- Column
    Table *-- Row
    Table *-- Constraint
    Table *-- Index
    Table --> PartitionStrategy : delegates routing
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
