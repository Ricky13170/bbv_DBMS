from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiResponse
from ..services.storage_service import StorageService

class ColumnListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=['Metadata & Table'],
        responses={
            200: OpenApiResponse(description="Danh sách Columns của Table"),
            404: OpenApiResponse(description="Không tìm thấy Table")
        },
        description="Lấy mô tả siêu dữ liệu (metadata) của tất cả cột nằm trong Bảng (table_name)."
    )
    def get(self, request, table_name):
        data = StorageService.get_columns_in_table(table_name)
        if data is None:
            return Response({"error": f"Bảng '{table_name}' không tồn tại!"}, status=status.HTTP_404_NOT_FOUND)
        return Response(data, status=status.HTTP_200_OK)

