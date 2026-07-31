from django.contrib import admin
from django.urls import path, include

from api.views.auth_views import LoginAPIView, RegisterAPIView
from api.views.system_views import SystemStatusAPIView, MonitoringAPIView
from api.views.database_views import DatabaseListAPIView, DatabaseDetailAPIView
from api.views.schema_views import SchemaListAPIView, SchemaDetailAPIView
from api.views.table_views import TableLoadAPIView, TableListAPIView, TableDetailAPIView
from api.views.column_views import ColumnListAPIView
from api.views.row_views import RowListAPIView
from api.views.query_views import QueryExecuteAPIView, QueryDynamicAPIView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    path('api/v1/login', LoginAPIView.as_view()),
    path('api/v1/register', RegisterAPIView.as_view()),
    path('api/v1/system/status', SystemStatusAPIView.as_view()),
    path('api/v1/monitoring/metrics', MonitoringAPIView.as_view()),
    path('api/v1/databases', DatabaseListAPIView.as_view()),
    path('api/v1/databases/<str:db_name>', DatabaseDetailAPIView.as_view()),
    path('api/v1/databases/<str:db_name>/schemas', SchemaListAPIView.as_view()),
    path('api/v1/databases/<str:db_name>/schemas/<str:schema_name>', SchemaDetailAPIView.as_view()),
    path('api/v1/schemas/<str:schema_name>/tables', TableListAPIView.as_view()),
    path('api/v1/schemas/<str:schema_name>/tables/<str:table_name>', TableDetailAPIView.as_view()),
    path('api/v1/tables/<str:table_name>/columns', ColumnListAPIView.as_view()),
    path('api/v1/tables/<str:table_name>/rows', RowListAPIView.as_view()),
    path('api/v1/databases/<str:db_name>/schemas/<str:schema_name>/tables/<str:table_name>', TableLoadAPIView.as_view()),

    path('api/v1/query/execute', QueryExecuteAPIView.as_view()),
    path('api/v1/query', QueryDynamicAPIView.as_view()),
]
