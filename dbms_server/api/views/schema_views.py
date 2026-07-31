from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiResponse
from ..services.storage_service import StorageService
from ..serializers import SchemaCreateSerializer

class SchemaListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=['Schema Management'],
        responses={
            200: OpenApiResponse(description="Danh sách các Schemas có trong Database"),
            404: OpenApiResponse(description="Không tìm thấy Cơ sở dữ liệu tương ứng")
        },
        description="Lấy danh sách các Schemas nằm trong một Database (db_name). Yêu cầu JWT Token."
    )
    def get(self, request, db_name):
        data = StorageService.get_schemas_in_database(db_name)
        if data is None:
            return Response(
                {"error": f"Cơ sở dữ liệu '{db_name}' không tồn tại trong hệ thống."}, 
                status=status.HTTP_404_NOT_FOUND
            )
        return Response(data, status=status.HTTP_200_OK)
        
    @extend_schema(
        tags=['Schema Management'],
        request=SchemaCreateSerializer,
        responses={
            201: OpenApiResponse(description="Khởi tạo Schema thành công"),
            400: OpenApiResponse(description="Schema đã tồn tại hoặc CSDL không đúng")
        },
        description="CREATE SCHEMA: Tạo một Namespace/Role mới (như public, schema1,...) bên trong CSDL để cô lập dữ liệu. Yêu cầu JWT Token."
    )
    def post(self, request, db_name):
        serializer = SchemaCreateSerializer(data=request.data)
        if serializer.is_valid():
            schema_name = serializer.validated_data['name']
            success = StorageService.create_schema(db_name, schema_name)
            if success:
                return Response(
                    {"message": f"Schema '{schema_name}' đã được khởi tạo theo CSDL '{db_name}' thành công!"}, 
                    status=status.HTTP_201_CREATED
                )
            return Response(
                {"error": f"Tạo thất bại! CSDL '{db_name}' không tồn tại hoặc Schema '{schema_name}' đã bị trùng tên."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SchemaDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=['Schema Management'],
        responses={
            200: OpenApiResponse(description="Xoá Schema thành công"),
            404: OpenApiResponse(description="Không tìm thấy Schema/Database tương ứng")
        },
        description="DROP SCHEMA: Lệnh xoá sổ triệt bỏ Schema cùng toàn bộ (Tables, Views...) cấu trúc trong nó. Siêu cực kỳ nguy hiểm. Yêu cầu JWT Token."
    )
    def delete(self, request, db_name, schema_name):
        success = StorageService.drop_schema(db_name, schema_name)
        if not success:
            return Response(
                {"error": f"Xóa thất bại! Không tìm thấy Schema '{schema_name}' bên trong CSDL '{db_name}'."}, 
                status=status.HTTP_404_NOT_FOUND
            )
        return Response(
            {"message": f"Toàn bộ vùng Schema '{schema_name}' thuộc CSDL '{db_name}' đã bị xoá trắng khỏi hệ thống!"}, 
            status=status.HTTP_200_OK
        )

