
from django.contrib import admin
from django.urls import path, include
from ninja import NinjaAPI, Router

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", include("apps.api.urls")),
]
