# DBMS REST API Documentation

This document specifies all endpoints of the **DBMS REST API v1** system. This API system serves as the communication and presentation layer between external clients and the core Database Management System (Storage Engine, Query Processing).

## Core API Catalog

Below is a comprehensive list of the APIs that will be built and applied in the system, including a simple example (for daily use) and an advanced example (for complex operations like mapping, filtering, joining, and pagination):

| Domain | Method | Endpoint | Description | Simple Example | Advanced Example |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Auth** | POST | `/auth/login` | Authenticate & Issue Token | `/auth/login` | (Issue Refresh/Access JWT securely) |
| **Auth** | POST | `/auth/register` | Register new user | `/auth/register` | (Register with role and profile data) |
| **System** | GET | `/system/status` | DBMS health check | `/system/status` | `/system/status?include_disk_usage=true` |
| **Database** | POST | `/databases` | Create a new database | `/databases` (Body: {name: 'SalesDB'}) | |
| **Database** | GET | `/databases` | List databases | `/databases` | `/databases?page=1&pageSize=20&filter=status eq 'Online'&sort=name` |
| **Database** | GET | `/databases/{dbName}` | Get database details | `/databases/SalesDB` | `/databases/SalesDB?expand=schemas,tables&fields=name,size,status` |
| **Database** | DELETE | `/databases/{dbName}` | Drop database | `/databases/SalesDB` | |
| **Schema** | POST | `/databases/{dbName}/schemas` | Create schema | `/databases/SalesDB/schemas` (Body: {name: 'sales'}) | |
| **Schema** | GET | `/databases/{dbName}/schemas` | List schemas | `/databases/SalesDB/schemas` | `/databases/SalesDB/schemas?search=sales&page=1&pageSize=20` |
| **Schema** | DELETE | `/databases/{dbName}/schemas/{schemaName}` | Drop schema | `/databases/SalesDB/schemas/sales` | |
| **Table** | POST | `/schemas/{schema}/tables` | Create Table | `/schemas/sales/tables` (Body: schema def) | |
| **Table** | GET | `/schemas/{schema}/tables` | List tables | `/schemas/sales/tables` | `/schemas/sales/tables?filter=rowCount gt 100000&sort=-rowCount` |
| **Table** | DELETE | `/schemas/{schema}/tables/{tableName}` | Drop table | `/schemas/sales/tables/Customers` | |
| **Column** | POST | `/tables/{table}/columns` | Add Column | `/tables/Customers/columns` (Body: column def) | |
| **Column** | GET | `/tables/{table}/columns` | List columns | `/tables/Customers/columns` | `/tables/Customers/columns?fields=name,type,isNullable` |
| **Column** | PUT | `/tables/{table}/columns/{column}` | Alter Column | `/tables/Customers/columns/age` (Body) | |
| **Column** | DELETE | `/tables/{table}/columns/{column}` | Drop Column | `/tables/Customers/columns/age` | |
| **Row** | POST | `/tables/{table}/rows` | Insert Row | `/tables/Customers/rows` (Body) | Insert multiple rows (batch insert) |
| **Row** | GET | `/tables/{table}/rows` | Query table data | `/tables/Customers/rows` | `/tables/Customers/rows?page=2&pageSize=50&filter=country eq 'Australia'` |
| **Row** | PUT | `/tables/{table}/rows/{rowId}` | Update Row | `/tables/Customers/rows/123` (Body) | |
| **Row** | DELETE | `/tables/{table}/rows/{rowId}` | Delete Row | `/tables/Customers/rows/123` | |
| **Query** | POST | `/query/execute` | Execute SQL | `SELECT * FROM Customers` (Body) | Multi-table JOIN with pagination, aggregation, filtering, and sorting (Body) |
| **Query** | POST | `/query` | Execute dynamic query | Select from one table | Join Customers -> Orders -> OrderItems -> Products with groupBy, having, and includeTotal=true |
| **Index** | GET | `/tables/{table}/indexes` | List indexes | `/tables/Orders/indexes` | `/tables/Orders/indexes?fields=name,type,fragmentation` |
| **View** | GET | `/views` | List views | `/views` | `/views?search=Sales&expand=dependencies` |
| **Procedure** | POST | `/procedures/{name}/execute`| Execute stored procedure | `/procedures/SyncCustomer/execute` | `/procedures/GenerateMonthlyReport/execute?async=true` |
| **Transaction**| GET | `/transactions` | Active transactions | `/transactions` | `/transactions?filter=status eq 'Running'&sort=startTime` |
| **Transaction**| POST | `/transactions/{id}/commit`| Drop/Commit Transaction | `/transactions/TX_123/commit` | Force transaction closure if deadlock occurs |
| **Backup** | POST | `/backup` | Create backup | `/backup` | `/backup?type=full&compress=true&storage=LocalDisk` |
| **Monitoring** | GET | `/monitoring/metrics` | Performance metrics | `/monitoring/metrics` | `/monitoring/metrics?from=2026-01-01&to=2026-01-31&groupBy=database` |
| **Security** | GET | `/users` | List users | `/users` | `/users?expand=roles,permissions&filter=status eq 'Enabled'` |
| **Audit** | GET | `/audit/logs` | Query audit logs | `/audit/logs` | `/audit/logs?filter=user eq 'admin'&from=2026-01-01&to=2026-01-31&pageSize=100` |

---

## Deployment Architecture

All APIs listed above will strictly follow the **Controller - Service - Repository (CSR)** pattern, mapped to Django REST Framework:
1. `api/urls.py`: Handles URL routing and path parameters.
2. `api/serializers.py`: Sanitizes and validates input data (prevents SQL Injection, type mismatches).
3. `api/views.py`: Acts as the **Controller**. Extracts requests and delegates to services.
4. `api/services.py`: The **Business Logic** bridge. Contains domain logic.
5. `src/*`: Acts as the **Repository**. Interacts directly with the underlying I/O and files.
