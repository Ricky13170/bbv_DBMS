from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from src.storage_engine.storage_engine import StorageEngine

class LoginAPIView(APIView):
    """
    API đăng nhập (Login) cực kỳ đơn giản để cấp Token.
    Áp dụng: Authentication (Ai đang hỏi?)
    """
    permission_classes = [AllowAny] # Login

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        if username == "admin" and password == "bbv_123":
            return Response({
                "message": "Login success!",
                "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.dummy_token_123"
            }, status=status.HTTP_200_OK)
        
        return Response({"error": "Tài khoản hoặc Mật khẩu sai"}, status=status.HTTP_401_UNAUTHORIZED)


class SystemStatusAPIView(APIView):
    """
    API kiểm tra sức khỏe hệ thống lõi.
    Áp dụng: Authorization (Chỉ người có token mới xem được)
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        engine_status = "RUNNING" 
        return Response({
            "status": engine_status,
            "user_requesting": request.user.username,
            "message": "Chiến cơ Storage Engine đang gầm rú!"
        })


class TableLoadAPIView(APIView):
    """
    API Load cấu trúc 1 Bảng (Load Table)
    Route: /api/v1/databases/{db}/schemas/{schema}/tables/{table}
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, db_name, schema_name, table_name):
        
        mock_table_schema = {
            "table_name": table_name,
            "database": db_name,
            "columns": ["id", "username", "created_at"],
            "row_count": 1050
        }
        
        return Response({
            "message": f"Tải thành công bảng {table_name}",
            "data": mock_table_schema
        })
