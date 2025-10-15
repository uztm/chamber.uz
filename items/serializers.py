from rest_framework import serializers
from .models import Category, Item


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class ItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Item
        fields = [
            'id',
            'image',
            'title',
            'caption',
            'link',
            'category',
            'created_at',
            'updated_at',
        ]
