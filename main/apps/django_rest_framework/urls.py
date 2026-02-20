from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from apps.content import views

urlpatterns = [
    path("categories/", views.CategoryList.as_view()),
    path("categories/<int:pk>/", views.CategoryDetail.as_view()),
    path("models/", views.ModelList.as_view()),
    path("models/<int:pk>/", views.ModelDetail.as_view()),
]
