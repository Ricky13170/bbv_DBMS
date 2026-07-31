from api.repositories.query_repository import QueryRepository

class QueryService:
    @staticmethod
    def execute_raw_sql(sql):
        if not sql or not str(sql).strip():
            return {"error": "Câu lệnh SQL rỗng hoặc không hợp lệ!"}
        return QueryRepository.execute_raw_sql(sql.strip())

    @staticmethod
    def execute_dynamic_query(payload):
        if not payload.get('table'):
            return {"error": "Bắt buộc phải truyền vào đích đến là tên Bảng (table)!"}
        return QueryRepository.execute_dynamic_query(payload)
