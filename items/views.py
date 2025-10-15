from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Category, Item
from .serializers import CategorySerializer, ItemSerializer


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """API: Only GET (list, retrieve) allowed for categories"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ItemViewSet(viewsets.ReadOnlyModelViewSet):
    """API: Only GET (list, retrieve) allowed for items with query filtering"""
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    def list(self, request, *args, **kwargs):
        """
        Custom filtering:
        - /api/items?category=CategoryName → filter by category name
        - /api/items?detail=itemId → return specific item by ID
        """
        category_name = request.query_params.get('category')
        detail_id = request.query_params.get('detail')

        # Filter by item ID (detail)
        if detail_id:
            try:
                item = Item.objects.get(id=detail_id)
                serializer = self.get_serializer(item)
                return Response(serializer.data)
            except Item.DoesNotExist:
                return Response({'detail': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)

        # Filter by category name
        queryset = self.queryset
        if category_name:
            queryset = queryset.filter(category__name__iexact=category_name)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
