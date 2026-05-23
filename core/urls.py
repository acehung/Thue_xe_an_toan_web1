from django.contrib import admin
from django.urls import include, path
from api.views import index
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),  # Thêm đường dẫn cho trang web
    path('api/', include('api.urls')),
]