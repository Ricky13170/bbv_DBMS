from rest_framework import serializers

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=50, required=True)
    password = serializers.CharField(
        max_length=128, 
        required=True, 
        write_only=True
    )

    def validate_username(self, value):
        if "DROP" in value.upper() or "SELECT" in value.upper():
            raise serializers.ValidationError("Tên đăng nhập chứa ký tự độc hại (SQL Injection)!")
        return value


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=50, min_length=3)
    password = serializers.CharField(max_length=128, min_length=3)


class TableMetadataSerializer(serializers.Serializer):
    table_name = serializers.CharField()
    database = serializers.CharField()
    columns = serializers.ListField(child=serializers.CharField())
    row_count = serializers.IntegerField(min_value=0)

class DatabaseCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=50, required=True, min_length=2)

class SchemaCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=50, required=True, min_length=2)

class TableCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=50, required=True, min_length=2)
    columns = serializers.ListField(
        child=serializers.DictField(), 
        required=False,
        help_text="Danh sách định nghĩa cấu trúc mảng liệt kê các cột."
    )

class QueryExecuteSerializer(serializers.Serializer):
    sql = serializers.CharField(required=True, help_text="Câu lệnh SQL thô (ví dụ: SELECT * FROM KhachHang WHERE id=1)")

class QueryDynamicSerializer(serializers.Serializer):
    table = serializers.CharField(required=True, help_text="Tên Bảng cần truy xuất")
    select = serializers.ListField(child=serializers.CharField(), required=False, help_text="Mảng danh sách các cột cần lấy (bỏ trống tự hiểu là select *)")
    where = serializers.DictField(required=False, help_text="Bộ lọc điều kiện dạng Object JSON")
    order_by = serializers.CharField(required=False, help_text="Tiêu chí sắp xếp ASC/DESC")
    limit = serializers.IntegerField(required=False, min_value=1, help_text="Giới hạn số dòng")
