from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import ProductModelViewSet

router = SimpleRouter()
router.register('', ProductModelViewSet, basename='products')

urlpatterns = [
    path('', include(router.urls))
]