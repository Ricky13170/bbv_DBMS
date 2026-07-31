from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiResponse
from ..services.storage_service import StorageService
from ..serializers import DatabaseCreateSerializer

class DatabaseListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=['Database Management'],
        responses={
            200: OpenApiResponse(description="Danh sách các cơ sở dữ liệu hiện có trong hệ thống"),
            401: OpenApiResponse(description="Chưa xác thực Token")
        },
        description="Quét kho dữ liệu và trả về toàn bộ Database hệ thống đang giữ. Yêu cầu JWT Token."
    )
    def get(self, request):
        data = StorageService.get_all_databases()
        return Response(data, status=status.HTTP_200_OK)

    @extend_schema(
        tags=['Database Management'],
        request=DatabaseCreateSerializer,
        responses={
            201: OpenApiResponse(description="Khởi tạo Cơ sở dữ liệu thành công"),
            400: OpenApiResponse(description="Tên CSDL bị trùng hoặc input sai")
        },
        description="Lệnh CREATE DATABASE: Tạo ra một thư mục/khối không gian mới trên ổ cứng để chứa dữ liệu. Yêu cầu JWT Token."
    )
    def post(self, request):
        serializer = DatabaseCreateSerializer(data=request.data)
        if serializer.is_valid():
            db_name = serializer.validated_data['name']
            success = StorageService.create_database(db_name)
            
            if success:
                return Response(
                    {"message": f"Cơ sở dữ liệu '{db_name}' đã được khởi tạo (CREATE) thành công!"}, 
                    status=status.HTTP_201_CREATED
                )
            return Response(
                {"error": f"Cơ sở dữ liệu '{db_name}' đã tồn tại trong hệ thống. Vui lòng chọn tên khác."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DatabaseDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=['Database Management'],
        responses={
            200: OpenApiResponse(description="Thông tin chi tiết về Cơ sở dữ liệu"),
            404: OpenApiResponse(description="Không tìm thấy Cơ sở dữ liệu tương ứng")
        },
        description="Lấy thông tin và metadata chi tiết của một Cơ sở dữ liệu cụ thể dựa trên tên (db_name). Yêu cầu JWT Token."
    )
    def get(self, request, db_name):
        data = StorageService.get_database_details(db_name)
        if not data:
            return Response(
                {"error": f"Oops! Cơ sở dữ liệu '{db_name}' không tồn tại trong hệ thống."}, 
                status=status.HTTP_404_NOT_FOUND
            )
        return Response(data, status=status.HTTP_200_OK)

    @extend_schema(
        tags=['Database Management'],
        responses={
            200: OpenApiResponse(description="Xoá cơ sở dữ liệu thành công"),
            404: OpenApiResponse(description="Không tìm thấy Cơ sở dữ liệu tương ứng")
        },
        description="DROP DATABASE: Lệnh xoá sổ hoàn toàn một CSDL vật lý (db_name). Nguy hiểm, cần JWT Token."
    )
    def delete(self, request, db_name):
        success = StorageService.drop_database(db_name)
        if not success:
            return Response(
                {"error": f"Không tìm thấy Cơ sở dữ liệu '{db_name}' để xóa."}, 
                status=status.HTTP_404_NOT_FOUND
            )
        return Response({"message": f"Cơ sở dữ liệu '{db_name}' đã được thả (DROP) thành công!"}, status=status.HTTP_200_OK)

