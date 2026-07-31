from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from .services import AuthService, SystemService, StorageService
from .serializers import LoginSerializer

class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=LoginSerializer,
        responses={
            200: OpenApiResponse(description="Trả về JWT Access Token và Refresh Token"),
            400: OpenApiResponse(description="Sai định dạng input"),
            401: OpenApiResponse(description="Sai username hoặc password")
        },
        description="Đăng nhập để nhận Token xác thực."
    )
    def post(self, request):
        # BƯỚC 1: Validator (Giao cho Serializer chốt chặn, lọc SQL Injection)
        serializer = LoginSerializer(data=request.data)
        
        if serializer.is_valid():
            # BƯỚC 2: Rút cất Data đã được lọc sạch
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            
            # BƯỚC 3: Gọi Service để xử lý Auth và cấp Token
            result = AuthService.authenticate_user(username, password)
            
            if result:
                return Response(result, status=status.HTTP_200_OK)
            
            return Response({"error": "Tài khoản hoặc Mật khẩu sai"}, status=status.HTTP_401_UNAUTHORIZED)
            
        # Nếu Serializer bắt được chuỗi bẩn, lập tức báo lỗi HTTP 400
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SystemStatusAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='include_disk_usage', 
                type=OpenApiTypes.BOOL, 
                location=OpenApiParameter.QUERY, 
                description="Điền true nếu muốn API quét thêm dung lượng ổ đĩa lưu trữ"
            ),
        ],
        responses={
            200: OpenApiResponse(description="Trạng thái hệ thống hoạt động bình thường"),
            401: OpenApiResponse(description="Token hết hạn hoặc không hợp lệ")
        },
        description="Kiểm tra trạng thái sức khỏe của DBMS Engine. Yêu cầu đăng nhập gắn Token trên Header."
    )
    def get(self, request):
        # Đọc tham số include_disk_usage từ URL (Mặc định là false)
        include_disk_usage = request.query_params.get('include_disk_usage', 'false').lower() == 'true'
        
        # Uỷ quyền lấy dữ liệu cho SystemService
        result = SystemService.get_engine_status(request.user.username, include_disk=include_disk_usage)
        return Response(result, status=status.HTTP_200_OK)


class TableLoadAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses={
            200: OpenApiResponse(description="Chi tiết metadata của Table"),
            401: OpenApiResponse(description="Chưa xác thực Token")
        },
        description="Load cấu trúc 1 Bảng (TableSchema). Yêu cầu JWT Token."
    )
    def get(self, request, db_name, schema_name, table_name):
        # Service sẽ làm công việc đọc đĩa thông qua Repository (src/)
        data = StorageService.load_table_schema(db_name, schema_name, table_name)
        
        return Response({
            "message": f"Tải thành công bảng {table_name}",
            "data": data
        }, status=status.HTTP_200_OK)
