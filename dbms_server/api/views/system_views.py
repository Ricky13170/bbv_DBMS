from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from ..services.system_service import SystemService

class SystemStatusAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=['System Health'],
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
        include_disk_usage = request.query_params.get('include_disk_usage', 'false').lower() == 'true'
        
        result = SystemService.get_engine_status(request.user.username, include_disk=include_disk_usage)
        return Response(result, status=status.HTTP_200_OK)

class MonitoringAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=['System Health'],
        responses={
            200: OpenApiResponse(description="Dữ liệu Performance Metrics của Hệ thống")
        },
        description="Lấy thông số giám sát quá trình vận hành (Ram, CPU, IOPS). Yêu cầu JWT Token."
    )
    def get(self, request):
        data = SystemService.get_monitoring_metrics()
        return Response(data, status=status.HTTP_200_OK)

