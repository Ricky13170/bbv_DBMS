from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiResponse
from ..services.query_service import QueryService
from ..serializers import QueryExecuteSerializer, QueryDynamicSerializer

class QueryExecuteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=['Query Execution'],
        request=QueryExecuteSerializer,
        responses={
            200: OpenApiResponse(description="Truy vấn SQL thực thi thành công"),
            400: OpenApiResponse(description="Lỗi cú pháp SQL hoặc truy vấn bị chặn")
        },
        description="Thực thi một câu lệnh SQL thuần túy (Raw SQL). Payload sẽ được đẩy trực tiếp xuống SQL Parser/Executor của Storage Engine."
    )
    def post(self, request):
        serializer = QueryExecuteSerializer(data=request.data)
        if serializer.is_valid():
            sql = serializer.validated_data['sql']
            result = QueryService.execute_raw_sql(sql)
            if "error" in result:
                return Response(result, status=status.HTTP_400_BAD_REQUEST)
            return Response(result, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class QueryDynamicAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=['Query Execution'],
        request=QueryDynamicSerializer,
        responses={
            200: OpenApiResponse(description="Truy vấn động thành công"),
            400: OpenApiResponse(description="Lỗi cấu trúc hoặc logic dữ liệu")
        },
        description="Thực thi truy vấn thông qua JSON Payload. Cấu trúc dạng Object này giúp các framework Frontend ORM có thể map Data xuống trực tiếp mà không cần viết lệnh SQL chữ."
    )
    def post(self, request):
        serializer = QueryDynamicSerializer(data=request.data)
        if serializer.is_valid():
            payload = serializer.validated_data
            result = QueryService.execute_dynamic_query(payload)
            if "error" in result:
                return Response(result, status=status.HTTP_400_BAD_REQUEST)
            return Response(result, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
