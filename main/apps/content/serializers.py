from rest_framework import serializers
from .models import Category, Model


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'icon']


class CategoryCreateSerializer(serializers.ModelSerializer):
    icon = serializers.CharField(required=False, allow_null=True, allow_blank=True)

    class Meta:
        model = Category
        fields = ['name', 'description', 'icon']


class ModelReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Model
        fields = ['id', 'name', 'description', 'price', 'category', 'image']


class ModelCreateSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Category.objects.all(),
    )

    class Meta:
        model = Model
        fields = ['id', 'name', 'description', 'price', 'category', 'image']
