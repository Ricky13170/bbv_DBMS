## FEATURE PRIORITIZATION MATRIX (80/20 Rule)

Before determining Design Patterns, we prioritized the exact granular features mapped out in our Object System to determine architecture logically from business needs.

| Priority | Exact Feature from Table 1 | Problem & Architectural Need | Driving Design Pattern |
|:---|:---|:---|:---|
| **P1 (Core)** | **Catalog & Database Lifecycle** | Must strictly govern memory and initialization of DB instances. | **Singleton / Factory Method** |
| **P1 (Core)** | **Database Entry Point (API)** | Must shield the user from internal engines. | **Facade Pattern** |
| **P1 (Core)** | **Schema Management** | Drop Schema must cascade correctly to Tables/Views. | **Composite Pattern** |
| **P1 (Core)** | **Table Creation** | Avoid monstrous constructors for Tables & Columns. | **Nested Builder Pattern** |
| **P1 (Core)** | **Row Data / Column Definition** | Prevent dirty parallel modifications. | **Value Object** |
| **P2 (Advanced)** | **Constraint Validation / Ref Integrity** | Disentangle raw validation logic (Cascades, Unique limits) out of Table. | **Strategy Pattern** |
| **P2 (Advanced)** | **Index Creation** | Instantiate varying hash/tree algorithms without hardcoding. | **Factory Method** |
| **P2 (Advanced)** | **Data Partitioning** | Route data segments seamlessly. | **Strategy Pattern** |
| **P3 (Extra)** | **Auto Increment ID** | Safe concurrent auto-numbering. | **State Pattern** |
| **P3 (Extra)** | **Virtual Tables (View)** | Alias complex queries as standard Tables. | **Proxy / Adapter Pattern** |
| **P3 (Extra)** | **Executable Logic (Procedure)** | Store ad-hoc script execution logic. | **Command Pattern** |
