from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import health, CustomerViewSet, PolicyViewSet, ClaimViewSet

router = DefaultRouter()
router.register(r'customers', CustomerViewSet, basename='customer')
router.register(r'policies', PolicyViewSet, basename='policy')
router.register(r'claims', ClaimViewSet, basename='claim')

urlpatterns = [
    path('health/', health, name='Health'),
    path('', include(router.urls)),
]
