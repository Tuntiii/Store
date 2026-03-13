from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from apps.content.views import CategoryListCreateView, ModelListCreateView

urlpatterns = [
    
    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('models/', ModelListCreateView.as_view(), name='model-list-create'),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
