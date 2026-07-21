# Advanced Architecture: Design Patterns & Unit Testing Roadmap

This document outlines the core Design Patterns derived from the Feature Mindmap, Class Mindmap, and Test Cases. It defines the rationale for applying these patterns and how they integrate into the Test-Driven Development (TDD) lifecycle.

---

## TABLE 1: DATABASE OBJECTS (Logical Schema Layer)

| Feature / Class | Design Pattern | Problem & Rationale | Unit Test (TDD) Implementation Strategy |
| :--- | :--- | :--- | :--- |
| **Catalog Management**<br>`CatalogManager` | **Singleton** | The database instance must have one centralized, globally accessible registry for all schemas to prevent synchronization conflicts. | Test accessing the instance from multiple parallel threads to ensure only one memory address is generated. |
| **Table Creation**<br>`SchemaBuilder`, `TableBuilder` | **Nested Builder** | Initializing a hierarchy (Schema contains Tables, Tables contain Columns) is bulky. Nested Builders allow cascading fluent configurations. | Test the fluent method chaining (`.with_table().with_column().build()`) to verify it returns a valid composite tree without missing nodes. |
| **Constraint Validation**<br>`IConstraintValidator` | **Strategy** | Extracts validation logic (NotNull, Unique) away from the `Table` class, preventing the `InsertRow` method from bloating with if/else chains. | Test using isolated Mock strategies or simulated bad data rows to catch specific `Exception` violations. |
| **Index Creation**<br>`IndexFactory` | **Factory Method** | The DBMS supports various Index types (Hash, B-Tree). The core system shouldn't hardcode their instantiation. | Call the Factory with a flag (`type="BTREE"`) and test if the inserted Node correctly routes through the B-Tree logic flow. |

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
