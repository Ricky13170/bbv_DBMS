from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiResponse
from ..services.auth_service import AuthService
from ..serializers import LoginSerializer, RegisterSerializer

class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        tags=['Authentication'],
        request=LoginSerializer,
        responses={
            200: OpenApiResponse(description="Trả về JWT Access Token và Refresh Token"),
            400: OpenApiResponse(description="Sai định dạng input"),
            401: OpenApiResponse(description="Sai username hoặc password")
        },
        description="Đăng nhập để nhận Token xác thực."
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            
            result = AuthService.authenticate_user(username, password)
            
            if result:
                return Response(result, status=status.HTTP_200_OK)
            
            return Response({"error": "Tài khoản hoặc Mật khẩu sai"}, status=status.HTTP_401_UNAUTHORIZED)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RegisterAPIView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        tags=['Authentication'],
        request=RegisterSerializer,
        responses={
            201: OpenApiResponse(description="Tạo tài khoản thành công"),
            400: OpenApiResponse(description="Tài khoản đã tồn tại hoặc định dạng input sai")
        },
        description="Đăng ký một tài khoản mới và lưu vào cơ sở dữ liệu ảo (data.json)."
    )
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            
            result = AuthService.register_user(username, password)
            
            if result:
                return Response(result, status=status.HTTP_201_CREATED)
            
            return Response({"error": "Tài khoản đã tồn tại!"}, status=status.HTTP_400_BAD_REQUEST)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

