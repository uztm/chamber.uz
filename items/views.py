from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
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

    def get_queryset(self):
        """
        Override get_queryset to handle filtering
        """
        queryset = Item.objects.all()
        category_name = self.request.query_params.get('category')

        if category_name:
            queryset = queryset.filter(category__name__iexact=category_name)

        return queryset

    def list(self, request, *args, **kwargs):
        """
        Custom filtering:
        - /api/items/ → all items
        - /api/items?category=CategoryName → filter by category name
        - /api/items?detail=itemId → return specific item by ID
        """
        detail_id = request.query_params.get('detail')

        # If detail parameter is provided, return single item
        if detail_id:
            try:
                item = Item.objects.get(id=detail_id)
                serializer = self.get_serializer(item)
                return Response(serializer.data)
            except Item.DoesNotExist:
                return Response(
                    {'detail': 'Item not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
            except ValueError:
                return Response(
                    {'detail': 'Invalid item ID'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        # Otherwise return filtered queryset
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)