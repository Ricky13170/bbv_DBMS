from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiResponse
from ..services.storage_service import StorageService

class RowListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=['Records & Data'],
        responses={
            200: OpenApiResponse(description="Danh sách dữ liệu các hàng trong Bảng"),
            404: OpenApiResponse(description="Không tìm thấy Table")
        },
        description="Trích xuất toàn bộ bản ghi (Rows) từ trong một Bảng (table_name)."
    )
    def get(self, request, table_name):
        data = StorageService.get_rows_in_table(table_name)
        if data is None:
            return Response({"error": f"Bảng '{table_name}' không tồn tại!"}, status=status.HTTP_404_NOT_FOUND)
        return Response(data, status=status.HTTP_200_OK)

