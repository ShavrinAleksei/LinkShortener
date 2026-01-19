from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('l/', include("apps.link_shortener.urls", namespace="link_shortener"))
]
