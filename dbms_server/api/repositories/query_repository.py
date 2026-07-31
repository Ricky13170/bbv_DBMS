class QueryRepository:
    @staticmethod
    def execute_raw_sql(sql):
        if "DROP" in sql.upper() or "DELETE" in sql.upper():
            return {
                "message": "Câu lệnh DML/DDL thành công",
                "affected_rows": 1,
                "execution_time_ms": 2.4
            }
        return {
            "sql": sql,
            "status": "success",
            "execution_time_ms": 12.5,
            "affected_rows": 2,
            "data": [
                {"id": 1, "col1": "Dữ liệu mô phỏng 1", "col2": 500},
                {"id": 2, "col1": "Dữ liệu mô phỏng 2", "col2": 1500}
            ]
        }

    @staticmethod
    def execute_dynamic_query(payload):
        return {
            "query_type": "Dynamic JSON",
            "table": payload.get('table'),
            "status": "success",
            "execution_time_ms": 8.0,
            "affected_rows": 1,
            "data": [
                {"id": 99, "col1": f"Dynamic Data cho bảng {payload.get('table')}"}
            ]
        }
