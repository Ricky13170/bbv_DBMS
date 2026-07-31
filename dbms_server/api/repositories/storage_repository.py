class StorageRepository:
    """
    Repository phụ trách tương tác với dữ liệu vật lý.
    Tạm thời mock dữ liệu tĩnh. Sau này sẽ gọi trực tiếp vào lõi FileManager/PageManager của DBMS.
    """
    
    @staticmethod
    def get_all_databases():
        return [
            {
                "name": "master",
                "status": "Online",
                "size_mb": 5.2,
                "created_at": "2026-07-01T10:00:00Z"
            },
            {
                "name": "sales",
                "status": "Online",
                "size_mb": 512.0,
                "created_at": "2026-07-15T08:30:00Z"
            },
            {
                "name": "hr",
                "status": "Online",
                "size_mb": 45.5,
                "created_at": "2026-07-20T14:20:00Z"
            }
        ]

    @staticmethod
    def get_database_details(db_name):
        valid_dbs = ["master", "sales", "hr"]
        if db_name.lower() in valid_dbs:
            return {
                "name": db_name,
                "size_mb": 512,
                "status": "Online",
                "created_at": "2026-01-15T08:30:00Z"
            }
        return None

    @staticmethod
    def create_database(db_name):
        valid_dbs = ["master", "sales", "hr"]
        if db_name.lower() in valid_dbs:
            return False
        # TODO: os.makedirs(f"data/{db_name}")
        return True

    @staticmethod
    def drop_database(db_name):
        valid_dbs = ["master", "sales", "hr"]
        if db_name.lower() in valid_dbs:
            # TODO: shutil.rmtree(f"data/{db_name}")
            return True
        return False

    @staticmethod
    def get_schemas_in_database(db_name):
        valid_dbs = ["master", "sales", "hr"]
        if db_name.lower() not in valid_dbs:
            return None
        return [
            {"name": "public", "table_count": 12},
            {"name": "internal", "table_count": 3}
        ]

    @staticmethod
    def create_schema(db_name, schema_name):
        valid_dbs = ["master", "sales", "hr"]
        if db_name.lower() not in valid_dbs:
            return False
            
        existing_schemas = ["public", "internal"]
        if schema_name.lower() in existing_schemas:
            return False
            
        return True

    @staticmethod
    def drop_schema(db_name, schema_name):
        valid_dbs = ["master", "sales", "hr"]
        if db_name.lower() not in valid_dbs:
            return False
            
        existing_schemas = ["public", "internal"]
        if schema_name.lower() not in existing_schemas:
            return False
            
        return True

    @staticmethod
    def get_tables_in_schema(schema_name):
        valid_schemas = ["public", "internal"]
        if schema_name.lower() not in valid_schemas:
            return None
        return [
            {"name": "KhachHang", "row_count": 1500, "size_mb": 2.5},
            {"name": "SanPham", "row_count": 300, "size_mb": 1.2},
            {"name": "HoaDon", "row_count": 45000, "size_mb": 15.8}
        ]

    @staticmethod
    def create_table(schema_name, table_name, columns=None):
        valid_schemas = ["public", "internal"]
        if schema_name.lower() not in valid_schemas:
            return False
            
        existing_tables = ["khachhang", "sanpham", "hoadon", "sys_config"]
        if table_name.lower() in existing_tables:
            return False
            
        return True

    @staticmethod
    def drop_table(schema_name, table_name):
        valid_schemas = ["public", "internal"]
        if schema_name.lower() not in valid_schemas:
            return False
            
        existing_tables = ["khachhang", "sanpham", "hoadon", "sys_config"]
        if table_name.lower() not in existing_tables:
            return False
            
        return True

    @staticmethod
    def get_table_metadata(table_name):
        return {
            "table_name": table_name,
            "database": "sales",
            "columns": ["id", "name", "price", "created_at"],
            "row_count": 300
        }

    @staticmethod
    def get_rows_in_table(table_name):
        # Mock data records
        return [
            {"id": 1, "name": "Laptop Dell", "price": 1500, "created_at": "2026-07-01"},
            {"id": 2, "name": "Chuột Logitech", "price": 25, "created_at": "2026-07-05"}
        ]
