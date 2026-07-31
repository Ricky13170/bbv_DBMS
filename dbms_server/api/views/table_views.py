from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiResponse
from ..services.storage_service import StorageService
from ..serializers import TableCreateSerializer

class TableLoadAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=['Metadata & Table'],
        responses={
            200: OpenApiResponse(description="Chi tiết metadata của Table"),
            401: OpenApiResponse(description="Chưa xác thực Token")
        },
        description="Load cấu trúc 1 Bảng (TableSchema). Yêu cầu JWT Token."
    )
    def get(self, request, db_name, schema_name, table_name):
        data = StorageService.load_table_schema(db_name, schema_name, table_name)
        
        return Response({
            "message": f"Tải thành công bảng {table_name}",
            "data": data
        }, status=status.HTTP_200_OK)

class TableListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=['Metadata & Table'],
        responses={
            200: OpenApiResponse(description="Danh sách các Bảng (Tables) có trong Schema"),
            404: OpenApiResponse(description="Không tìm thấy Schema tương ứng")
        },
        description="Lấy danh sách các bảng (Tables) chứa trong một Schema (schema_name). Yêu cầu JWT Token."
    )
    def get(self, request, schema_name):
        data = StorageService.get_tables_in_schema(schema_name)
        if data is None:
            return Response(
                {"error": f"Schema '{schema_name}' không tồn tại. Vui lòng kiểm tra lại."}, 
                status=status.HTTP_404_NOT_FOUND
            )
        return Response(data, status=status.HTTP_200_OK)

    @extend_schema(
        tags=['Metadata & Table'],
        request=TableCreateSerializer,
        responses={
            201: OpenApiResponse(description="Tạo Bảng thành công"),
            400: OpenApiResponse(description="Bảng đã tồn tại hoặc Schema không đúng")
        },
        description="CREATE TABLE: Khởi tạo bảng dữ liệu mới bám vào Schema. Yêu cầu JWT Token."
    )
    def post(self, request, schema_name):
        serializer = TableCreateSerializer(data=request.data)
        if serializer.is_valid():
            table_name = serializer.validated_data['name']
            columns = serializer.validated_data.get('columns', [])
            success = StorageService.create_table(schema_name, table_name, columns)
            if success:
                return Response(
                    {"message": f"Bảng '{table_name}' đã được khởi tạo theo Schema '{schema_name}' thành công!"}, 
                    status=status.HTTP_201_CREATED
                )
            return Response(
                {"error": f"Tạo thất bại! Schema '{schema_name}' chưa có hoặc Bảng '{table_name}' đã bị trùng lặp."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TableDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=['Metadata & Table'],
        responses={
            200: OpenApiResponse(description="Xoá Bảng thành công"),
            404: OpenApiResponse(description="Không tìm thấy Bảng tương ứng")
        },
        description="DROP TABLE: Lệnh triệt tiêu hoàn toàn một Bảng và các Records bên trong. Yêu cầu JWT Token."
    )
    def delete(self, request, schema_name, table_name):
        success = StorageService.drop_table(schema_name, table_name)
        if not success:
            return Response(
                {"error": f"Xóa thất bại! Bảng '{table_name}' không được tìm thấy bên trong Schema '{schema_name}'."}, 
                status=status.HTTP_404_NOT_FOUND
            )
        return Response(
            {"message": f"Bảng khổng lồ '{table_name}' đã bị đập nát (DROP) thành công khỏi hệ thống!"}, 
            status=status.HTTP_200_OK
        )

