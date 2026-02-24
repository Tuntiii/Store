from rest_framework.generics import ListCreateAPIView
from .models import Category, Model
from .serializers import CategorySerializer, ModelReadSerializer, ModelCreateSerializer


class CategoryListCreateView(ListCreateAPIView):
    serializer_class = CategorySerializer

    def get_queryset(self):
        queryset = Category.objects.all()
        contain = self.request.query_params.get('contain')
        if contain is not None:
            queryset = queryset.filter(name__icontains=contain)
        return queryset


class ModelListCreateView(ListCreateAPIView):
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ModelCreateSerializer
        return ModelReadSerializer

    def get_queryset(self):
        queryset = Model.objects.select_related('category').all()
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        category = self.request.query_params.get('category')

        if min_price is not None:
            queryset = queryset.filter(price__gte=float(min_price))
        if max_price is not None:
            queryset = queryset.filter(price__lte=float(max_price))
        if category is not None:
            queryset = queryset.filter(category__name=category)

        return queryset
