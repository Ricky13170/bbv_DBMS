import shutil

class SystemService:
    @staticmethod
    def get_engine_status(username, include_disk=False):
        response = {
            "status": "RUNNING",
            "dbms_version": "DBMS_bbv v1.0",
            "user_requesting": username,
            "message": "Chiến cơ Storage Engine đang gầm rú!"
        }
        
        if include_disk:
            total, used, free = shutil.disk_usage("/")
            response["disk_usage"] = {
                "total_gb": round(total / (1024**3), 2),
                "used_gb": round(used / (1024**3), 2),
                "free_gb": round(free / (1024**3), 2)
            }
            
        return response

    @staticmethod
    def get_monitoring_metrics():
        return {
            "cpu_usage_percent": 14.5,
            "memory_usage_mb": 1024.5,
            "active_connections": 12,
            "iops_read": 1450,
            "iops_write": 350,
            "uptime_seconds": 36000
        }

