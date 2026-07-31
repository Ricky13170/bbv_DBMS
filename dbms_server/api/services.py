# Cấu trúc Service để tách riêng rẽ Logic Nghiệp Vụ khỏi Controller (views.py)
# Service (services.py) làm nhiệm vụ gọi trực tiếp xuống Repository (thư mục src/)

from src.storage_engine.storage_engine import StorageEngine
import shutil

from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

class AuthService:
    """
    Xử lý các nghiệp vụ chung liên quan đến xác thực.
    """
    @staticmethod
    def authenticate_user(username, password):
        # Kết nối với danh sách Users của Django (SQLite/DB)
        user = authenticate(username=username, password=password)
        
        if user is not None:
            # Nếu pass đúng, sinh JWT Token bảo mật!
            refresh = RefreshToken.for_user(user)
            return {
                "message": "Login success!",
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh)
            }
        return None


class SystemService:
    """
    Quản lý các nghiệp vụ đo lường, giám sát chung của DBMS.
    """
    @staticmethod
    def get_engine_status(username, include_disk=False):
        # Khởi tạo mock status của DB
        response = {
            "status": "RUNNING",
            "dbms_version": "DBMS_bbv v1.0",
            "user_requesting": username,
            "message": "Chiến cơ Storage Engine đang gầm rú!"
        }
        
        # Nếu bật flag Disk Usage, quét dung lượng ổ đĩa thật
        if include_disk:
            total, used, free = shutil.disk_usage("/")
            response["disk_usage"] = {
                "total_gb": round(total / (2**30), 2),
                "used_gb": round(used / (2**30), 2),
                "free_gb": round(free / (2**30), 2)
            }
            
        return response


class StorageService:
    """
    Xử lý các nghiệp vụ liên quan đến việc đọc/ghi Table, Schema từ Storage Engine.
    """
    @staticmethod
    def load_table_schema(db_name, schema_name, table_name):
        # Chỗ này bạn sẽ khởi tạo FileManager từ phía Repository 
        # Ví dụ:
        # file_manager = FileManager(base_dir=f"data/{db_name}")
        # return file_manager.read_table_info(table_name)
        
        # Trả về mock data cho hiện tại
        return {
            "table_name": table_name,
            "database": db_name,
            "columns": ["id", "username", "created_at"],
            "row_count": 1050
        }
