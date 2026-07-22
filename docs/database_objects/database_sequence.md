# Design Documents: Database & DatabaseCatalog

## Pattern Assignment
| Class | Pattern | Rationale |
|:---|:---|:---|
| `Database` | **Facade** | Hides `CatalogManager` + `SchemaBuilder` behind a clean, single API |
| `DatabaseCatalog` | **Factory Method** | Controls Database object creation and lifecycle (create / drop / get) |

---

## Step 4: Sequence Diagram — `DatabaseCatalog.create_database`

```mermaid
sequenceDiagram
    participant Client
    participant DC as DatabaseCatalog (Factory)
    participant DB as Database (Facade)
    participant CM as CatalogManager (Singleton)

    Client->>DC: create_database("Tiki")
    activate DC
    DC->>DC: Check if "Tiki" already exists
    alt Already exists
        DC-->>Client: raise DatabaseExistsException
    else New database
        DC->>DB: new Database("Tiki")
        activate DB
        DB-->>DC: Database instance
        deactivate DB
        DC->>DC: Store in _databases dict
        DC-->>Client: return Database object
    end
    deactivate DC
```

---

## Step 4: Sequence Diagram — `Database.create_schema`

```mermaid
sequenceDiagram
    participant Client
    participant DB as Database (Facade)
    participant SB as SchemaBuilder
    participant CM as CatalogManager (Singleton)

    Client->>DB: db.create_schema("public")
    activate DB
    DB->>SB: SchemaBuilder("public").build()
    activate SB
    SB-->>DB: Schema object
    deactivate SB
    DB->>CM: add_schema(schema)
    activate CM
    CM-->>DB: success
    deactivate CM
    DB-->>Client: void
    deactivate DB
```
