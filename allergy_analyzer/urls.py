from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('user_management.urls')),
    path('api/', include('user_management.urls')),   # Include API routes

]
