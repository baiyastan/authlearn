from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied

from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer


class CategoryListCreateView(generics.ListCreateAPIView):
    """Категорияларды көрүү жана жаңы категория кошуу."""
    queryset = Category.objects.all().order_by("name")
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]


class ProductListCreateView(generics.ListCreateAPIView):
    """Бардык продуктуларды көрүү жана жаңы продукт кошуу."""
    queryset = Product.objects.select_related("owner", "category").prefetch_related("images").order_by("-created_at")
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

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
