from rest_framework import serializers

class LoginSerializer(serializers.Serializer):
    """
    Serializer làm nhiệm vụ canh gác (Validation) cho cổng Login.
    Diễn giải: Trước khi data lọt được vào Views, nó phải qua đây!
    """
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


class TableMetadataSerializer(serializers.Serializer):
    """
    Serializer ép kiểu mớ bùi nhùi từ StorageEngine thành JSON chuẩn chỉnh.
    """
    table_name = serializers.CharField()
    database = serializers.CharField()
    columns = serializers.ListField(child=serializers.CharField())
    row_count = serializers.IntegerField(min_value=0)
