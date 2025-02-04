from rest_framework.viewsets import ModelViewSet
from .models import Product
from .serializers import ProductSerializer, ProductImageSerializer


class ProductModelViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request  # Pass request for validation
        return context


# class ProductImageModelViewSet(ModelViewSet):
#     queryset = Product.objects.all()
#     serializer_class = ProductImageSerializer
    
#     def get_serializer_context(self):
#         context = super().get_serializer_context()
#         context["request"] = self.request  # Pass request for validation
#         return context