from api.repositories.storage_repository import StorageRepository

class StorageService:
    @staticmethod
    def get_all_databases():
        return StorageRepository.get_all_databases()

    @staticmethod
    def get_database_details(db_name):
        return StorageRepository.get_database_details(db_name)

    @staticmethod
    def create_database(db_name):
        return StorageRepository.create_database(db_name)

    @staticmethod
    def drop_database(db_name):
        return StorageRepository.drop_database(db_name)

    @staticmethod
    def get_schemas_in_database(db_name):
        return StorageRepository.get_schemas_in_database(db_name)

    @staticmethod
    def create_schema(db_name, schema_name):
        return StorageRepository.create_schema(db_name, schema_name)

    @staticmethod
    def drop_schema(db_name, schema_name):
        return StorageRepository.drop_schema(db_name, schema_name)

    @staticmethod
    def get_tables_in_schema(schema_name):
        return StorageRepository.get_tables_in_schema(schema_name)

    @staticmethod
    def create_table(schema_name, table_name, columns=None):
        return StorageRepository.create_table(schema_name, table_name, columns)

    @staticmethod
    def drop_table(schema_name, table_name):
        return StorageRepository.drop_table(schema_name, table_name)

    @staticmethod
    def get_table_metadata(table_name):
        return StorageRepository.get_table_metadata(table_name)

    @staticmethod
    def get_rows_in_table(table_name):
        return StorageRepository.get_rows_in_table(table_name)
