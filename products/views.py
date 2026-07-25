from django.db import models
from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied

from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer


class CategoryListCreateView(generics.ListCreateAPIView):
    """Категорияларды көрүү жана жаңы категория кошуу."""
    queryset = Category.objects.all().order_by("name")
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None


class ProductListCreateView(generics.ListCreateAPIView):
    """Бардык продуктуларды көрүү жана жаңы продукт кошуу.

    Query параметрлери:
        search — name же description боюнча издөө
        category — category id боюнча фильтр
    """
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = Product.objects.select_related("owner", "category").prefetch_related("images").order_by("-created_at")
        search = self.request.query_params.get("search")
        if search:
            qs = qs.filter(
                models.Q(name__icontains=search) | models.Q(description__icontains=search)
            )
        category = self.request.query_params.get("category")
        if category:
            qs = qs.filter(category_id=category)
        return qs

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Продуктту көрүү, өзгөртүү, жок кылуу (ээси гана өзгөртө/жок кыла алат)."""
    queryset = Product.objects.select_related("owner", "category").prefetch_related("images")
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        if serializer.instance.owner != self.request.user:
            raise PermissionDenied("Сиз бул продуктту өзгөртө албайсыз.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.owner != self.request.user:
            raise PermissionDenied("Сиз бул продуктту жок кыла албайсыз.")
        instance.delete()
